import logging

def classify_item(name: str) -> str:
    name = name.lower()
    if "coaching" in name:
        return "coaching"
    elif "shipping" in name:
        return "shipping"
    elif "outbound" in name:
        return "outbound"
    elif "rollover" in name:
        return "rollover"
    return "supplement"

def apply_classification(df):

    logging.info("Applying item classification.")
    df_copy = df.copy()  # this avoids changing the original DataFrame
    df_copy['category'] = df_copy['item_name'].apply(classify_item)
    return df_copy
