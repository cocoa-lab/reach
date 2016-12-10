setwd("C:users/Tyler/dropbox/leelab/experiments/exp_files/reach")
wd = getwd()
input_dir   <- paste(wd, "/data/",   sep = "", collapse = "")
output_dir  <- paste(wd, "/output/", sep = "", collapse = "")

train1_file <- "_reach_train1_output.csv"
train2_file <- "_reach_train2_output.csv"
test_file   <- "_reach_test_output.csv"

sub_int     <- readline(prompt = "Enter subject number as integer: ")
sub_string  <- toString(sub_int)

sub_train1_file <- paste(input_dir, sub_string, train1_file, sep = "", collapse = "")
sub_train2_file <- paste(input_dir, sub_string, train2_file, sep = "", collapse = "")
sub_test_file   <- paste(input_dir, sub_string, test_file,   sep = "", collapse = "")

raw_train1_behav <- read.csv(sub_train1_file)
raw_train2_behav <- read.csv(sub_train2_file)
raw_test_behav   <- read.csv(sub_test_file) 



