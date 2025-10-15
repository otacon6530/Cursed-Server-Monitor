CREATE TRIGGER trg_Server_LastModified
ON [dbo].[Server]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE s
    SET s.LastModified = GETDATE()
    FROM [dbo].[Server] s
    INNER JOIN inserted i ON s.ServerId = i.ServerId;
END;