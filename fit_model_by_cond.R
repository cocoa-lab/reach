
# **********
# IMPORTANT NOTE:
# Condition Sep Pen
# 0         32  0
# 1         44  0 
# 2         32  1
# 3         44  1
# 4         32  3
# 5         44  3
# 6         32  5
# 7         44  5
# 8         32  15
# 9         44  15

#ORDERED BASED ON ABOVE CONDITION CODING SCHEME
PENALTIES   <- c(0, 0, 1, 1, 3, 3, 5, 5, 15, 15)
SEPERATIONS <- c(32, 44, 32, 44, 32, 44, 32, 44, 32, 44)
MULTIPLIERS <- c(0, 0, 0, 0, 1, 1, 0, 0, 1, 1)
FACTORS     <- c(0, 0, 1, 1, 1, 1, 5, 5, 5, 5)
#subs omitted: 407 (crazy high lambda), 410 & 500 (abs(lambda) < 1)
subs   <- c(403, 404, 405, 406, 411, 412, 501, 502, 503, 504, 505, 506) 
wd = getwd()
fitness_frame <- data.frame()
#vectors for storing mean AIC values for each condition; one vector for each model 
conds            <- c()
pens             <- c()
seps             <- c()
mults            <- c()
facts            <- c()
lambs            <- c()
stds             <- c()
loss_all_aic     <- c()
all_sub          <- c()
no_loss_all_aic  <- c()
for (mod in c('Y', 'N')){
    for (cond in c(0, 2, 4, 6, 8, 1, 3, 5, 7, 9)) {
    	if (mod == 'Y'){
    		conds <- c(conds, rep(cond, length(subs)))
	        pens  <- c(pens, rep(PENALTIES[cond + 1], length(subs)))
	        seps  <- c(seps, rep(SEPERATIONS[cond + 1], length(subs)))
	        mults <- c(mults, rep(MULTIPLIERS[cond + 1], length(subs)))
	        facts <- c(facts, rep(FACTORS[cond + 1], length(subs)))
    	}
		for (sub in subs) { 
   #          print("Model Type")
	  #       print("--------")
	  #       print(mod)
	  #       print("Condition")
	  #       print("--------")
	  #       print(cond)
			# print("Subject:")
	  #       print("--------")
	  #       print(sub)
	        
	        sub_string <- toString(sub)
	        
	        standard_dir  <- paste(wd, '/standard_data/', sub_string, '_', 'standard_test_data.csv', sep = "", collapse = "")
	        standard_data <- read.csv(standard_dir)
	        loss_aversion <- -mean(standard_data[["LossAversion"]])
	        standard_dev  <- sqrt(mean(standard_data[["train1_var"]]))

	        
            dev_input_dir <- paste(wd, '/', sub_string, '_', mod, '_deviance_input.csv', sep = "", collapse = "")
	        raw_dev_data  <- read.csv(dev_input_dir)
	        dev_data   <- raw_dev_data[raw_dev_data$"cond" == cond,]
	        poke_vec   <- dev_data$"poke"
	        est_vec    <- dev_data$"est"
	        std_vec    <- dev_data$"std"


	        dev <- (-2)*sum( dnorm( 
	        	        poke_vec,
	        	        mean = est_vec, 
	        	        sd   = std_vec,
	        	        log  = TRUE))
	        
	        if (mod == 'Y') {
	        	p <- 2
	        } else {
	        	p <- 1
	        }

	        sub_aic <- dev + 2*p

	        if((cond == 0) & (sub == 404)){
	        	print(mod)
	        	print(dev)
	        	print(sub_aic)
	        }


	        if (mod == 'Y') {
				loss_all_aic <- c(loss_all_aic, sub_aic)
				lambs <- c(lambs, loss_aversion)
	            stds  <- c(stds, standard_dev)
	            #c_stds <- c(c_stds, cond_std)	
	            all_sub <- c(all_sub, sub)        
			} else {
                no_loss_all_aic <- c(no_loss_all_aic, sub_aic)	
	        } 
	    }     
	}
}
aic_diffs <- c()
for (i in c(1:length(loss_all_aic))){
	diff      <- loss_all_aic[i] - no_loss_all_aic[i]
	aic_diffs <- c(aic_diffs, diff)
}
print("SEPS LENGTH")
print(length(seps))
print("LAMBS LENGTH")
print(length(lambs))


fitness_frame <- data.frame(L_minus_N = aic_diffs, loss_aversion = loss_all_aic,
                            no_loss_aversion = no_loss_all_aic, sep_dist = seps,
                            pen_val = pens, mult = mults, factor = facts, 
                            lambda = lambs, std = stds, subject = all_sub)

output_dir    <- paste(wd, 'aic_files/model_AICs_by_condition.csv', sep = "", collapse = "")
write.csv(fitness_frame, file = output_dir, row.names = FALSE)
