# SATD-repay
## Still working on updating the **readme**. Will finish soon!
Taxonomy and SATD repayment model (DLRepay) from the paper: Towards the Repayment of Self-Admitted Technical Debt [1].
<br><br>
Link to the data and output of our study:
https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link
<br><br>
This repo contains the following directories:
1. **codebase**: consists of the following main components:
   - *SATD-R*: Source code for creating the main dataset of this study (SATD-R).
   - *A-BigFix*: Source code for creating the transfer learning dataset (A-BigFix). NNGen [2] was used to annotate A-BigFix.
   - *DLRepay*: Source code for conducting DLRepay experiments for SATD repayment.
   - *prepare_unixcoder_data*: Source code for data preparation for baseline (UniXcoder [3]) experiments.
   - *unixcoder_for_satd_repay*: Source code for conducting baseline experiments for SATD repayment.
2. **data**: consists of the directories of SATD-R, A-BigFix, and along with their metadata, supporting data, and original data. Due to the excessive size, the actual folder and its content can be found [here](https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link) under "data.zip".
   - The original data used for creating SATD-R was first curated by Maldonado et al. [4] and further developed by Zampetti et al [5].
   - We used BigFix [6] for transfer learning.
4. **emp_study**:
   - contains our analysis towards answering RQ1 and RQ2 regarding the *purpose* and *helpfulness* of the SATD comment in repaying the technical debt.
   - Can also be found [here](https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link) under the "Taxonomy - Purpose and Helpfulness" sheets.
   - The resulting taxonomy answering RQ1 & RQ2.
   - The agreement calculation of the taxonomy between two judges (J1 & J2).
5. **output**: consists of the directories of the results of the evaluation measures and generated SATD repayments for DLRepay and UniXcoder within various experiments. It also consists of the directories of the saved UniXcoder models. Due to the excessive size, the actual folder and its content can be found [here](https://drive.google.com/drive/folders/1KCG0V2FOnUcdzR-Huqb_9wJwsI3pQqzR?usp=share_link) under "output.zip".

<hr>

If you use any of our material, please consider citing us:
```
@article{alhefdhi4441278towards,
  title={Towards the Repayment of Self-Admitted Technical Debt},
  author={Alhefdhi, Abdulaziz Hasan M and Dam, Hoa Khanh and Ghose, Aditya},
  journal={Available at SSRN 4441278}
}
```

<hr>

[1] A. Alhefdhi, H. K. Dam, A. Ghose, Towards the Repayment of Self-Admitted Technical Debt, Available at SSRN 4441278, 2023.

[2] Z. Liu, X. Xia, A. E. Hassan, D. Lo, Z. Xing, X. Wang, Neural-machine-translation-based commit message generation: how far are we?, in: Proceedings of the 33rd ACM/IEEE International Conference on Automated Software Engineering, 2018, pp. 373–384.

[3] D. Guo, S. Lu, N. Duan, Y. Wang, M. Zhou, J. Yin, Unixcoder: Unified cross-modal pre-training for code representation, arXiv preprint arXiv:2203.03850, 2022.

[4] E. d. S. Maldonado, R. Abdalkareem, E. Shihab, A. Serebrenik, An empirical study on the removal of self-admitted technical debt, in: Software Maintenance and Evolution (ICSME), 2017 IEEE International Conference on, IEEE, 2017, pp. 238–248.

[5] F. Zampetti, A. Serebrenik, M. Di Penta, Was self-admitted technical debt removal a real removal? an in-depth perspective, in: 2018 IEEE/ACM 15th International Conference on Mining Software Repositories (MSR), IEEE, 2018, pp. 526–536.

[6] Y. Li, S. Wang, T. N. Nguyen, Dlfix: Context-based code transformation learning for automated program repair, in: Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering, 2020, pp. 602–614.
