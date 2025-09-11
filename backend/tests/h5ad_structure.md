```
/                      # 루트 (하나의 AnnData)
├─ X                  # n_obs × n_vars 행렬(표현행렬; dense 또는 sparse)
├─ obs/               # 행(셀) 메타데이터: 각 열이 개별 dataset
│  ├─ <col_1>
│  ├─ <col_2>
│  └─ ...
├─ var/               # 열(유전자) 메타데이터: 각 열이 개별 dataset
│  ├─ <col_1>
│  ├─ <col_2>
│  └─ ...
├─ obs_names          # 각 셀의 이름(index)
├─ var_names          # 각 유전자의 이름(index)
├─ layers/            # 추가 층(예: "counts", "log1p")
│  ├─ counts
│  ├─ log1p
│  └─ ...
├─ obsm/              # 셀×k 행렬들(저차원 좌표 등): 예) X_pca, X_umap
│  ├─ X_pca
│  └─ X_umap
├─ varm/              # 유전자×k 행렬들(예: PCA 로딩)
│  └─ PCs
├─ obsp/              # 셀×셀 pairwise 행렬(인접그래프 등)
│  ├─ distances
│  └─ connectivities
├─ varp/              # 유전자×유전자 pairwise 행렬
├─ uns/               # 비정형 메타데이터(dict 유사; 플롯 색상, 파라미터, 카테고리 등)
│  └─ neighbors/ ...  # 예: k, metric, connectivities/params 등
└─ raw/               # 원시표현(raw) 서브트리(있을 때만)
   ├─ X
   ├─ var/
   └─ var_names
   ```