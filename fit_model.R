
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


wd = getwd()
fitness_frame <- data.frame()
model_fits<- c()
for (mod in c('Y', 'N')){
    
	all_aic <- c()
    
    #subs omitted: 407 (crazy high lambda), 410 & 500 (abs(lambda) < 1)
	for (sub in c(403, 404, 405, 406, 411, 412, 501, 502, 503, 504, 505, 506)) {#
		print("Subject:")
        print("--------")
        print(sub)
        print("Model Type")
        print("--------")
        print(mod)

        sub_string <- toString(sub)
        input_dir  <- paste(wd, '/deviance_files/', sub_string, '_', mod, '_deviance_input.csv', sep = "", collapse = "")
        dev_data   <- read.csv(input_dir)

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
        all_aic <- c(all_aic, sub_aic)

	}
    print(all_aic)
	model_aic  <- mean(all_aic)
    model_fits <- c(model_fits, model_aic)
}

fitness_frame <- data.frame(loss_aversion = model_fits[1], no_loss_aversion = model_fits[2])
output_dir    <- paste(wd, '/aic_files/', 'model_AICs_total.csv', sep = "", collapse = "")
write.csv(fitness_frame, file = output_dir, row.names = FALSE)
