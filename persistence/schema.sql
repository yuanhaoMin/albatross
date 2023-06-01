IF OBJECT_ID('dbo.app_user') IS NULL
    CREATE TABLE app_user (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        access_bitmap INT NOT NULL,
        created_time DATETIME,
        last_login_time DATETIME,
    );

IF OBJECT_ID('dbo.openai_completion') IS NULL
    CREATE TABLE openai_completion (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT UNIQUE,
        prompt NVARCHAR(MAX),
        prompt_template NVARCHAR(MAX),
        template_args NVARCHAR(MAX),
        model VARCHAR(255),
        temperature DECIMAL(3,2),
        update_time DATETIME,
        FOREIGN KEY (user_id) REFERENCES app_user(id),
    );

IF OBJECT_ID('dbo.openai_chat_completion') IS NULL
    CREATE TABLE openai_chat_completion (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT UNIQUE,
        messages NVARCHAR(MAX),
        model VARCHAR(255),
        temperature DECIMAL(3,2),
        update_time DATETIME,
        FOREIGN KEY (user_id) REFERENCES app_user(id),
    );