erDiagram
    User ||--o{ Inventory : "食材在庫の持ち主"
    Category ||--o{ Inventory : "商品のカテゴリ"
    User ||--o{ Category : "カテゴリーの持ち主"
    User ||--o{ ShoppingList : "買い物リストの持ち主"
    User ||--o{ Menu : "メニューの持ち主"
    User ||--o{ MenuMaterial : "メニュー材料の持ち主"
    Category ||--o{ MenuMaterial : "メニュー材料のカテゴリ"
    Menu }o--o{ MenuMaterialMenu : "メニューの材料"
    MenuMaterial }o--o{ MenuMaterialMenu : "メニュー材料のメニュー"
    User ||--o{ MenuMaterialMenu : "メニュー材料メニュー中間の持ち主"
    User ||--o{ WastedMaterial : "廃棄材料の持ち主"
    Category ||--o{ WastedMaterial : "廃棄材料のカテゴリ"
    User {
        int id PK "ユーザID"
        varchar(64) username "ユーザ名"
        varchar(128) password_hash "パスワードハッシュ"
        date created_at "作成日"
    }
    Category {
        int id PK "カテゴリID"
        int user_id FK "ユーザー名"
        varchar(64) category_name "カテゴリ名"
    }
    Inventory {
        int id PK "在庫ID"
        int user_id FK "ユーザID"
        int category_id FK "カテゴリID"
        varchar(128) product_name "商品名"
        int quantity "数量"
        date purchase_date "購入日"
        date expiration_date "賞味期限"
    }
    ShoppingList {
        int id PK "買い物リストID"
        int user_id FK "ユーザID"
        varchar(128) name "商品名"
        int quantity "数量"
        date created_at "作成日"
    }
    Menu {
        int id PK "メニューID"
        int user_id FK "ユーザID"
        varchar(128) name "メニュー名"
    }
    MenuMaterial {
        int id PK "メニュー材料ID"
        int user_id FK "ユーザID"
        varchar(128) name "材料名"
        int category_id FK "カテゴリID"
    }
    MenuMaterialMenu{
        int menu_id FK "メニューID"
        int menu_material_id FK "メニュー材料ID"
        int user_id FK "ユーザID"
    }
    WastedMaterial {
        int id PK "廃棄材料ID"
        int user_id FK "ユーザID"
        int category_id FK "カテゴリID"
        varchar(128) name "材料名"
        int quantity "数量"
        date created_at "作成日"
    }
    
