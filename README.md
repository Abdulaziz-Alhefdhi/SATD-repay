# SATD-repay
## Still working on updating the **readme**. Will finish soon!
Taxonomy and SATD repayment model (DLRepay) from the paper: Towards the Repayment of Self-Admitted Technical Debt [1].
<br><br>
Link to the data and output of our study:
https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link
<br><br>
This repo contains the following directories:
1. **codebase**: consists of the following main components:
   - Source code for creating the main dataset for this study (SATD-R).
   - Source code for creating the transfer learning dataset (A-BigFix). NNGen [4] was used to annotate A-BigFix.
   - Source code for DLRepay experiments.
   - Source code for data preparation for baseline (UniXcoder) experiments
2. text
3. **stud_prep.zip**: Contains the following:
   - The original data curated by [2] and further developed by [3].
   - The code used to process it and create the main dataset of the study (SATD-R).
   - The resulted main dataset of our study, SATD-R (satd_repayment.pkl).
4. **Taxonomy - Purpose and Helpfulness**: Contains the following:
   - Our empirical study to answer RQ1 and RQ2 in the paper.
   - The resulted taxonomy that answers RQ1 & RQ2.
   - Agreement calculation
5. **nngen.zip**: Contains our employment of NNGen [4] in our transfer learning approach. It contains the following:
   - BigFix [5]: the dataset used for our transfer learning approach (bigfix folder).
   - Our code to use NNGen to annotote BigFix.
6. **dlrepay.zip**: Contains the following:
   - Annotated BigFix (A-BigFix).
   - The code and results of variuos experiments using our proposed model (DLRepay), some of which were reported in the Evaluation section of the paper (RQ3 & RQ4).
   - The code to prepare the data for RQ5
7. **unixcoder.zip**: Contains the code, models, and results used for the camparative study (RQ5) using the baseline (UniXcoder [6]).
<hr>

[1] A. Alhefdhi, H. K. Dam, A. Ghose, Towards the Repayment of Self-Admitted Technical Debt, (submitted to) Information and Software Technology (2023).

[2] Z. Liu, X. Xia, A. E. Hassan, D. Lo, Z. Xing, X. Wang, Neural-machine-translation-based commit message generation: how far are we?, in: Proceedings of the 33rd ACM/IEEE International Conference on Automated Software Engineering, 2018, pp. 373–384.

[3] E. d. S. Maldonado, R. Abdalkareem, E. Shihab, A. Serebrenik, An empirical study on the removal of self-admitted technical debt, in: Software Maintenance and Evolution (ICSME), 2017 IEEE International Conference on, IEEE, 2017, pp. 238–248.

[4] F. Zampetti, A. Serebrenik, M. Di Penta, Was self-admitted technical debt removal a real removal? an in-depth perspective, in: 2018 IEEE/ACM 15th International Conference on Mining Software Repositories (MSR), IEEE, 2018, pp. 526–536.

[5] Y. Li, S. Wang, T. N. Nguyen, Dlfix: Context-based code transformation learning for automated program repair, in: Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering, 2020, pp. 602–614.
