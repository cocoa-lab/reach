#CONSTANTS
#number of pokes to simulate around each aim point
SIM_SIZE  = 600
SEP_DISTS = c(32, 44)
PEN_VALS  = c(0, -1, -3, -5, -15)
RADIUS    = rep(32, SIM_SIZE)

#file suffixes
DATA_FILE  = "all_behav_model_data.csv"
EF_SUFF    = "earnings.csv"
output_dir = "/estimated_earnings/"

#vectors for target position
TARG_X    = rep(0, SIM_SIZE)
TARG_Y    = rep(0, SIM_SIZE)

#vectors for penalty position
PEN_Y     = rep(0, SIM_SIZE)

wd = getwd()

#FUNCTIONS
#computes distance between pairs of vectors of equal length 
dist2D = function(x1, y1, x2, y2) {
    dist = (sqrt((x2 - x1)^2 + (y2 - y1)^2))
    return(dist)
}

insertRow = function(existingDF, newrow, r) {
  existingDF[seq(r+1,nrow(existingDF)+1),] = existingDF[seq(r,nrow(existingDF)),]
  existingDF[r,] = newrow
  return(existingDF)
}

#given vector of distances from the penalty center
#decides whether point represented by this distance is within the penalty circle
#returns vector of these decisions
isPen = function(pen_dist) {
    pen_poke = pen_dist < RADIUS
    return(pen_poke)
}
#given vector of distances from the target center
#decides whether point represented by this distance is within the target circle
#returns vector of these decisions
isTarg = function(targ_dist) {
    targ_poke = targ_dist < RADIUS
    return(targ_poke)
}
#given vectors of decisions about whether a point is inside the target and penalty circles
#decides whether the point is inside both circles
#returns vector of these decisions
targAndPen = function(targ_poke, pen_poke) {
    targ_pen_poke = targ_poke & pen_poke
}

#given an (x,y) aim point, N number of pokes, poke variability, penalty value, and separation distance
#simulates N pokes around aimpoint and computes and returns the mean earnings (i.e., expected value)
getCondEarnings = function(aim_point, num_pokes, poke_var, pen, sep_dist) {

    if (pen == -3 | pen == -15) {
        rew = 3
    } else {
        rew = 1
    }
    #generate gaussian distributions around the grid point
    x_sample   = rnorm(num_pokes, mean = aim_point[1], sd = poke_var)
    y_sample   = rnorm(num_pokes, mean = aim_point[2], sd = poke_var)

    if (sep_dist == 32){
        pen_pos_x = rep(-32, SIM_SIZE)
    }
    else {
        pen_pos_x = rep(-44, SIM_SIZE)
    }

    pen_dists  = dist2D(x_sample, y_sample, pen_pos_x, PEN_Y)
    targ_dists = dist2D(x_sample, y_sample, TARG_X, TARG_Y)
    
    pen_pokes  = isPen(pen_dists)
    targ_pokes = isTarg(targ_dists)
    dual_pokes = targAndPen(targ_pokes, pen_pokes)
    
    #earnings for each sim poke: dual_poke -> pen+rew; pen_poke -> pen; targ_poke -> rew
    earnings   = ifelse(dual_pokes == TRUE, pen+rew, ifelse(pen_pokes == TRUE, pen, 
                  ifelse(targ_pokes == TRUE, rew, 0)))

    return(mean(earnings))
}
#given ordered vector of expected values, penalty value, and sep dist
#creates dataframe of aim points and their expected values (for specific pen and sep)
#saves this dataframe as csv for future input into EV landscape graph functions
writeEarnData = function(earnings, sub, aim_type){
    earnings.data = data.frame('32,0' = earnings[1], '32,1'  = earnings[2], '32,3' = earnings[3],
                              '32,5' = earnings[4], '32,15' = earnings[5], '44,0' = earnings[6],
                              '44,1' = earnings[7], '44,3'  = earnings[8], '44,5' = earnings[9],
                              '44,15' = earnings[10], 'total' = earnings[11])
    earn_data_file  = paste(output_dir, sub, '_', aim_type, '_', EF_SUFF,  sep = "", collapse = "")
    write.table(earnings.data, file = earn_data_file, row.names=FALSE, sep = ",")
}

#MAIN LOOP
all_data_file  = paste(wd, "/model_estimates/", DATA_FILE,  sep = "", collapse = "")
all_data_frame = read.csv(all_data_file)
for (sub_int in c(403, 404, 405, 406, 407, 410, 411, 412, 500,  501, 502, 503, 504, 505, 506)){ 
    sub_data = all_data_frame[all_data_frame$sub == sub_int,]
    for (aimpoints in c('CAVG','LTV', 'NLTV', 'LCV', 'NLCV')){
        print("Subject")
        print("--------")
        print(sub_int)

        print("Aimpoint type")
        print("--------")
        print(aimpoints)

        earnings = c()
        for (sep in SEP_DISTS){
            for (pen in PEN_VALS){
                    sf = sub_data[sub_data$sep_dist == sep,]
                    pf = sf[sf$pen_val == pen,]
                    if (aimpoints == 'CAVG'){
                        x_aim = sf[["avg_x"]]
                        y_aim = sf[["avg_y"]]
                    } elif (aimpoint == 'LTV'){
                        x_aim = sf[["ltv_x"]]
                        y_aim = sf[["ltv_y"]]
                    } elif (aimpoint == 'NLTV'){
                        x_aim = sf[["nltv_x"]]
                        y_aim = sf[["nltv_y"]]
                    } elif (aimpoint == 'LCV'){
                        x_aim = sf[["lcv_x"]]
                        y_aim = sf[["lcv_y"]]
                    } elif (aimpoint == 'NLCV'){
                        x_aim = sf[["nlcv_x"]]
                        y_aim = sf[["nlcv_y"]]
                    }

                    var     = mean(sf[["cond_var"]])
                    sd      = sqrt(var)

                    earning   = getCondEarnings([x_aim, y_aim], SIM_SIZE, sd, pen, sep)
                    earnings  = c(earnings, earning)
            }
        }
        total = sum(earnings)
        earnings = c(earnings, total)
        writeEarnData(earnings, sub_int, aimpoints)
    }
}    