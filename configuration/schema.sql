IF OBJECT_ID('dbo.app_user') IS NULL
    CREATE TABLE app_user (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        access_bitmap INT NOT NULL,
        created_time DATETIME,
        last_login_time DATETIME,
    );

IF OBJECT_ID('dbo.openai_user_completion') IS NULL
    CREATE TABLE openai_user_completion (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT UNIQUE,
        message NVARCHAR(MAX),
        history NVARCHAR(MAX),
        model VARCHAR(255),
        temperature DECIMAL(3,2),
        last_chat_time DATETIME,
        FOREIGN KEY (user_id) REFERENCES app_user(id),
    );