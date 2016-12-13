library(MASS)
wd = getwd()

sep_dists = c(32, 44)
pen_vals  = c(0, 1, 3, 5, 15)
models    = c('Y', 'N')

for (sub in c(403, 404, 405, 406, 411, 412, 501, 502, 503, 504, 505, 506)){
	for (mod in models){
		for (sep in sep_dists){
			for (pen in pen_vals){
		    	sub_string  <- toString(sub)
       	    	input_dir   <- paste(wd, '/model_output/', sub_string, '_',
       	    	                    mod, '_', sep, '_', pen, '_EV_graph_data.csv',
       	    	                    sep = "", collapse = "")
        		graph_data  <- read.csv(input_dir)
        		matrix_data <- as.matrix(graph_data)
        		ev_matrix    <- matrix(matrix_data[,3], nrow=201, ncol=201)
        		output_dir  <- paste(wd, '/ev_matrices/', sub_string, '_',
        			                mod, '_', sep, '_', pen, '_ev_matrix.txt',
        			                sep = "", collapse = "")
        		write.matrix(ev_matrix, output_dir)
			}
		}
	}
}