CREATE PROCEDURE [dbo].[SetService]
    @server VARCHAR(100),
    @Service VARCHAR(100),
    @Status VARCHAR(100) = ''
AS
BEGIN
    SET NOCOUNT ON;
    Declare @ServerId INT = (SELECT ServerId FROM [dbo].[Server] WHERE [Server] = @server)
    IF EXISTS (
        SELECT TOP 1 1 
            FROM [Service] a
        WHERE a.[ServerId] = @ServerId AND a.[Service] = @Service
    )
    BEGIN
        UPDATE a
        SET a.[Status] = @Status
        FROM [Service] a
        WHERE a.[ServerId] = @ServerId AND a.[Service] = @Service;
    END
    ELSE
    BEGIN
        INSERT INTO [Service] ([ServerId], [Service], [Status])
        VALUES (@ServerId, @Service, @Status);
    END

    RETURN 0
END