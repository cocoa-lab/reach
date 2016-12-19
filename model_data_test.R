#CONSTANTS
#number of pokes to simulate around each aim point
SIM_SIZE  <- 100
SEP_DISTS <- c(32, 44)
PEN_VALS  <- c(0, -1, -3, -5, -15)
RADIUS    <- rep(32, SIM_SIZE)

#file suffixes
GD_SUFFIX   <- "_EV_graph_data.csv"  
MD_SUFFIX   <- "_model_aim_estimates.csv"
EVD_SUFFIX  <- "_model_EV_estimates.csv"
SD_SUFFIX   <- "_standard_test_data.csv"

#grid of each aim point for simulation
XY_GRID   <- expand.grid(c(-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50), c(-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50))#c(-100:100), c(-100:100)

#vectors for target position
TARG_X    <- rep(0, SIM_SIZE)
TARG_Y    <- rep(0, SIM_SIZE)

#vectors for penalty position
PEN_Y     <- rep(0, SIM_SIZE)

# #GLOBAL VARIABLES
# #sub_int     <- readline(prompt = "Enter subject number as integer: ")
# sub_string  <- toString(sub_int)
# LA_input    <- readline(prompt = "Include loss aversion score (Y/N): ")

wd = getwd()
# input_dir   <- paste(wd, "/standard_data/", sub_string, sep = "", collapse = "")
# output_dir  <- paste(wd, "/model_output/",  sub_string, '_', LA_input, sep = "", collapse = "")

# sub_test_file   <- paste(input_dir, SD_SUFFIX,   sep = "", collapse = "")
# test_data_frame <- read.csv(sub_test_file)
# train_var       <- mean(test_data_frame[["train1_var"]])
# train_std       <- sqrt(train_var)

# if (LA_input == 'Y' | LA_input == 'y') {
#     loss_aversion <- -mean(test_data_frame[["LossAversion"]])
# } else {
#     loss_aversion <- 1
# }


#FUNCTIONS
#computes distance between pairs of vectors of equal length 
dist2D <- function(x1, y1, x2, y2) {
    dist <- (sqrt((x2 - x1)^2 + (y2 - y1)^2))
    return(dist)
}

insertRow <- function(existingDF, newrow, r) {
  existingDF[seq(r+1,nrow(existingDF)+1),] <- existingDF[seq(r,nrow(existingDF)),]
  existingDF[r,] <- newrow
  return(existingDF)
}

#given vector of distances from the penalty center
#decides whether point represented by this distance is within the penalty circle
#returns vector of these decisions
isPen <- function(pen_dist) {
    pen_poke <- pen_dist < RADIUS
    return(pen_poke)
}
#given vector of distances from the target center
#decides whether point represented by this distance is within the target circle
#returns vector of these decisions
isTarg <- function(targ_dist) {
    targ_poke <- targ_dist < RADIUS
    return(targ_poke)
}
#given vectors of decisions about whether a point is inside the target and penalty circles
#decides whether the point is inside both circles
#returns vector of these decisions
targAndPen <- function(targ_poke, pen_poke) {
    targ_pen_poke <- targ_poke & pen_poke
}

#given an (x,y) aim point, N number of pokes, poke variability, penalty value, and separation distance
#simulates N pokes around aimpoint and computes and returns the mean earnings (i.e., expected value)
getExpectedValue <- function(aim_point, num_pokes, poke_var, pen_val, sep_dist, lambda) {
  #  print("LA")
  #  print(lambda)
  #  print("Pen_val")
   # print(pen_val)
    pen <- pen_val*lambda
  #  print("pen")
   #print(pen)
    if (pen_val == -3 | pen_val == -15) {
        rew <- 3
    } else {
        rew <- 1
    }
    #generate gaussian distributions around the grid point
    x_sample   <- rnorm(num_pokes, mean = aim_point[1], sd = poke_var)
    y_sample   <- rnorm(num_pokes, mean = aim_point[2], sd = poke_var)

    if (sep_dist == 32){
        pen_pos_x <- rep(-32, SIM_SIZE)
    }
    else {
        pen_pos_x <- rep(-44, SIM_SIZE)
    }
            
    pen_dists  <- dist2D(x_sample, y_sample, pen_pos_x, PEN_Y)
    targ_dists <- dist2D(x_sample, y_sample, TARG_X, TARG_Y)
    
    pen_pokes  <- isPen(pen_dists)
    targ_pokes <- isTarg(targ_dists)
    dual_pokes <- targAndPen(targ_pokes, pen_pokes)
    
    #earnings for each sim poke: dual_poke -> pen+rew; pen_poke -> pen; targ_poke -> rew
    earnings   <- ifelse(dual_pokes == TRUE, pen+rew, ifelse(pen_pokes == TRUE, pen, 
                  ifelse(targ_pokes == TRUE, rew, 0)))

    return(mean(earnings))
}
#given ordered vector of expected values, penalty value, and sep dist
#creates dataframe of aim points and their expected values (for specific pen and sep)
#saves this dataframe as csv for future input into EV landscape graph functions
writeGraphData <- function(exp_vals, pen_val, sep_dist, lambda, std_train){
    graph_x          <- as.numeric(XY_GRID[, 1])
    graph_y          <- as.numeric(XY_GRID[, 2])
    mod_pen_rep      <- rep((pen_val*lambda), length(graph_x))
    sep_dist_rep     <- rep((sep_dist), length(graph_x))
    std_rep          <- rep((std_train), length(graph_x))
    
    graph.data       <- data.frame(x_aim = graph_x,  y_aim = graph_y, ev = exp_vals, mod_pen = mod_pen_rep, sep = sep_dist_rep, std = std_rep)
    print(graph.data)
    sep_string       <- toString(sep_dist)
    pen_val          <- abs(pen_val)
    pen_string       <- toString(pen_val)
    graph_data_file  <- paste(output_dir, '_', sep_string, '_', pen_string, GD_SUFFIX, sep = "", collapse = "")
    #write.table(graph.data, file = graph_data_file, row.names=FALSE, sep = ",")
}

#MAIN LOOP
#ommitted 407, 410, 500  ...  411, 412, 501, 502
for (sub_int in c(403)){ #  503, 504, 505, 506 , 404, 405, 406
    for (LA_input in c('Y', 'N')){

        print("Subject:")
        print("--------")
        print(sub_int)

        print("Model Type")
        print("--------")
        print(LA_input)
    
        sub_string  <- toString(sub_int)
        
        input_dir   <- paste(wd, "/standard_data/", sub_string, sep = "", collapse = "")
        output_dir  <- paste(wd, "/model_output/",  sub_string, '_', LA_input, sep = "", collapse = "")

        sub_test_file   <- paste(input_dir, SD_SUFFIX,   sep = "", collapse = "")
        test_data_frame <- read.csv(sub_test_file)
        train_var       <- mean(test_data_frame[["train1_var"]])
        train_std       <- sqrt(train_var)

        if (LA_input == 'Y') {
            loss_aversion <- -mean(test_data_frame[["LossAversion"]])
        } else {
            loss_aversion <- 1
        }
        print("Loss aversion score")
        print("-------------------")
        print(loss_aversion)
        
        for (sep in SEP_DISTS){
            sep_frame <- test_data_frame[test_data_frame$absoluteSepDist == sep,]
            for (pen in PEN_VALS){
                
                #empty list for storing EVs for the EV landscape graph (for this condition)
                graph_EVs <- c()

                #condition-specific subset of standardized dataframe
                pen_frame   <- sep_frame[sep_frame$penaltyVal == pen,]
                
                #gets the mean x and y endpoints from the standardized data
                avg_behav_x <- mean(pen_frame[["standardPokePosX"]])
                avg_behav_y <- mean(pen_frame[["standardPokePosY"]])
               
                #iterate through every point in the grid
                for (n in c(1:nrow(XY_GRID))){
                    temp_aim  <- as.numeric(XY_GRID[n,])
                    temp_ev   <- getExpectedValue(temp_aim, SIM_SIZE, train_std, pen, sep, loss_aversion)
                    graph_EVs <- c(graph_EVs, temp_ev)
                }
                #writeGraphData(graph_EVs, pen, sep, loss_aversion, train_std)
            }
        }
    }   
}    