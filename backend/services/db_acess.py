from sqlalchemy import create_engine
import pandas as pd

engine=create_engine("postgresql+psycopg2://postgres:post1234@localhost:5432/stockout_db",future=True)


def get_product_features(sku:str):
    """
    Recuperer les features du produit correspandant au SKU depuis Postgresql
    """
    query=f"""
    SELECT * FROM products_features  where  sku =%s
    """ 
    df=pd.read_sql(query, engine, params=(sku,))
    if df.empty: 
        return None
    else: 
        return df.iloc[0].to_dict() 


def get_all_products():
    """ recupere tous les produits dans la base de donnees"""
    query = "SELECT * FROM products_features "
    df=pd.read_sql(query, engine)

    if df.empty:
        return None
    else:
        return df.to_dict(orient="records")    
