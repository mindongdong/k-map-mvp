import scanpy as sc

adata = sc.read_h5ad("cell_by_bin.h5ad", backed='r')

adata.X
adata.obs
adata.var
adata.layers
adata.obsm
adata.uns

print(adata)
print(adata.obs.head())
print(adata.var.head())
