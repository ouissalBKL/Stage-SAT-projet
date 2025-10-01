from fastapi import APIRouter, HTTPException
from services.db_acess import get_product_features, get_all_products
from services.prediction_service import predict_from_features

router = APIRouter()


@router.get("/predict/all")
def predict_for_all_products():
    products = get_all_products()
    if not products:  # empty list ou None
        raise HTTPException(status_code=404, detail="No products found in database")

    results = []
    for product in products:
        sku = product.get("sku")
        features = {k: v for k, v in product.items() if k != "sku"}
        prediction = predict_from_features(features)
        print("prediction - predict.py:19")
        results.append(
            {
                "sku": sku,
                "prediction": prediction["prediction"],
                "probability": prediction["probability"],
            }
        )

    return results


@router.get("/predict/{sku}")
def predict_product_from_db(sku: str):
    features = get_product_features(sku)
    if features is None:
        raise HTTPException(status_code=404, detail="products not found")

    if "sku" in features:
        features.pop("sku")
    result = predict_from_features(features)
    print(result)
    return {"sku": sku, **result}
