Due to the excessive size, the actual content of this folder can be found [here](https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link) under "data.zip". This folder consists of the following directories:
- **A-BigFix**: consists of two folders:
   - *bigfix*: the original BigFix dataset.
   - *NNGen*: consists of the NNGen dataset as well as the annotated BigFix dataset (bigfix.test.diff & nngen.bigfix.test.msg).
- **SATD-R**: consists of the following:
   - The open source projects from which the original data were collected (camel, gerrit, hadoop, logging-log4j1, and tomcat).
   - The collected dataset (satd_removal.csv)
   - SATD-R, our dataset (satd_repayment.pkl and satd_repayment.csv)
- **UniXcoder**: consists of multiple directories representing multiple versions of the processed data for the baseline experiments. The folder names describe the essence of each experiment. For example, the *comment+code2code_train_bigfix* folder contains the processed data used for the experiment where both the comment and the code used as an input, the code as an output, and A-BigFix used for training.
