# SATD-repay
Taxonomy and SATD repayment model (DLRepay) from the paper: Towards the Repayment of Self-Admitted Technical Debt [1].
<hr>
Link to the data, codebase, and results of the paper:
https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link

In the link, you will find the following files:
1. **stud_prep.zip**: Contains the following:
  1.1. The original data curated by [2] and further developed by [3].
  1.2. The code used to process it and create the main dataset of the study (SATD-R).
  1.3. The resulted main dataset of our study, SATD-R (satd_repayment.pkl).
2. **Taxonomy - Purpose and Helpfulness**: Contains the following:
  2.1. Our empirical study to answer RQ1 and RQ2 in the paper.
  2.2. The resulted taxonomy that answers RQ1 & RQ2.
  2.3. Agreement calculation
3. **nngen.zip**: Contains our employment of NNGen [4] in our transfer learning approach. It contains the following:
  3.1. BigFix [5]: the dataset used for our transfer learning approach (bigfix folder).
  3.2. Our code to use NNGen to annotote BigFix.
4. **dlrepay.zip**: Contains the following:
  4.1. Annotated BigFix (A-BigFix).
  4.2. The code and results of variuos experiments using our proposed model (DLRepay), some of which were reported in the Evaluation section of the paper (RQ3 & RQ4).
  4.3. The code to prepare the data for RQ5
5. **unixcoder.zip**: Contains the code, models, and results used for the camparative study (RQ5) using the baseline (UniXcoder [6]).
<hr>

[1] A. Alhefdhi, H. K. Dam, A. Ghose, Towards the Repayment of Self-Admitted Technical Debt, (submitted to) Information and Software Technology (2023).

[2] E. d. S. Maldonado, R. Abdalkareem, E. Shihab, A. Serebrenik, An empirical study on the removal of self-admitted technical debt, in: Software Maintenance and Evolution (ICSME), 2017 IEEE International Conference on, IEEE, 2017, pp. 238–248.

[3] F. Zampetti, A. Serebrenik, M. Di Penta, Was self-admitted technical debt removal a real removal? an in-depth perspective, in: 2018 IEEE/ACM 15th International Conference on Mining Software Repositories (MSR), IEEE, 2018, pp. 526–536.

[4] Z. Liu, X. Xia, A. E. Hassan, D. Lo, Z. Xing, X. Wang, Neural-machine-translation-based commit message generation: how far are we?, in: Proceedings of the 33rd ACM/IEEE International Conference on Automated Software Engineering, 2018, pp. 373–384.

[5] Y. Li, S. Wang, T. N. Nguyen, Dlfix: Context-based code transformation learning for automated program repair, in: Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering, 2020, pp. 602–614.
