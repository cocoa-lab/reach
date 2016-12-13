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
				df <- read.csv(input_dir)
				md <- as.matrix(df)
				z  <- matrix(md[,3], nrow=201, ncol=201)
				x  <- matrix(c(-100:100), nrow=201, ncol=201)
				y  <- t(x)
				file <- paste(wd, "/graphs/", "/", sub, "/_", mod, "_", sep,
				              "_", pen, "_3D_ev_graph.pdf", sep="", collapse="")
				pdf(file)
				surf3D(x, y, z, col = jet.col(n = 100, alpha = 0.7),
					xlim=range(x), ylim=range(y), zlim=range(z),xlab='X',
					ylab='Y', zlab='Expected Value', scale=TRUE,theta=20, 
					phi=20, box=TRUE, ticktype='detailed',bty='b')
				dev.off()
			}
		}
	}
}



# output_dir  <- paste(wd, '/ev_matrices/', sub_string, '_',
# 									mod, '_', sep, '_', pen, '_ev_matrix.txt',
# 									sep = "", collapse = "")
# 				write.matrix(ev_matrix, output_dir)