# SATD-repay
## Still working on updating the **readme**. Will finish soon!
Taxonomy and SATD repayment model (DLRepay) from the paper: Towards the Repayment of Self-Admitted Technical Debt [1].
<br><br>
Link to the data and output of our study:
https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link
<br><br>
This repo contains the following directories:
1. **codebase**: consists of the following main components:
   - *SATD-R*: Source code for creating the main dataset for this study (SATD-R).
   - *A-BigFix*: Source code for creating the transfer learning dataset (A-BigFix). NNGen [2] was used to annotate A-BigFix.
   - *DLRepay*: Source code for conducting DLRepay experiments for SATD repayment.
   - *prepare_unixcoder_data*: Source code for data preparation for baseline (UniXcoder [3]) experiments.
   - *unixcoder_for_satd_repay*: Source code for conducting baseline experiments for SATD repayment.
2. **data**: consists of the directories of SATD-R, A-BigFix, and along with their metadata, supporting data, and original data. Due to the excessive size, the actual folder and its content can be found [here](https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link) under "data.zip".
3. **emp_study**:
   - contains our analysis towards answering RQ1 and RQ2 regarding the purpose and helpfulness of the SATD comment in repaying the technical debt.
   - Can also be found [here](https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link) under the "Taxonomy - Purpose and Helpfulness" sheets.
   - The resulting taxonomy answering RQ1 & RQ2.
   - The agreement calculation of the taxonomy between two judges (J1 & J2).
4. **output**



6. **stud_prep.zip**: Contains the following:
   - The original data curated by [4] and further developed by [5].
   - The code used to process it and create the main dataset of the study (SATD-R).
   - The resulted main dataset of our study, SATD-R (satd_repayment.pkl).
7. **Taxonomy - Purpose and Helpfulness**: Contains the following:
   - Our empirical study to answer RQ1 and RQ2 in the paper.
   - The resulted taxonomy that answers RQ1 & RQ2.
   - Agreement calculation
8. **nngen.zip**: Contains our employment of NNGen [2] in our transfer learning approach. It contains the following:
   - BigFix [6]: the dataset used for our transfer learning approach (bigfix folder).
   - Our code to use NNGen to annotote BigFix.
9. **dlrepay.zip**: Contains the following:
   - Annotated BigFix (A-BigFix).
   - The code and results of variuos experiments using our proposed model (DLRepay), some of which were reported in the Evaluation section of the paper (RQ3 & RQ4).
   - The code to prepare the data for RQ5
10. **unixcoder.zip**: Contains the code, models, and results used for the camparative study (RQ5) using the baseline (UniXcoder [6]).
<hr>

[1] A. Alhefdhi, H. K. Dam, A. Ghose, Towards the Repayment of Self-Admitted Technical Debt, Available at SSRN 4441278, 2023.

[2] Z. Liu, X. Xia, A. E. Hassan, D. Lo, Z. Xing, X. Wang, Neural-machine-translation-based commit message generation: how far are we?, in: Proceedings of the 33rd ACM/IEEE International Conference on Automated Software Engineering, 2018, pp. 373–384.

[3] D. Guo, S. Lu, N. Duan, Y. Wang, M. Zhou, J. Yin, Unixcoder: Unified cross-modal pre-training for code representation, arXiv preprint arXiv:2203.03850, 2022.

[4] E. d. S. Maldonado, R. Abdalkareem, E. Shihab, A. Serebrenik, An empirical study on the removal of self-admitted technical debt, in: Software Maintenance and Evolution (ICSME), 2017 IEEE International Conference on, IEEE, 2017, pp. 238–248.

[5] F. Zampetti, A. Serebrenik, M. Di Penta, Was self-admitted technical debt removal a real removal? an in-depth perspective, in: 2018 IEEE/ACM 15th International Conference on Mining Software Repositories (MSR), IEEE, 2018, pp. 526–536.

[6] Y. Li, S. Wang, T. N. Nguyen, Dlfix: Context-based code transformation learning for automated program repair, in: Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering, 2020, pp. 602–614.
