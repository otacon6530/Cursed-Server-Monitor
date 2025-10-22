CREATE PROCEDURE [dbo].[SetServerMetrics]
	@server VARCHAR(100),
	@RAMUsage INT = -1,
	@CPUUsage INT = -1,
	@DiskUsage INT = -1,
	@Uptime VARCHAR(100) = ''
AS
	INSERT INTO [log].[Server] ([ServerId], [RAMUsage], [CPUUsage], [DiskUsage])
	SELECT a.ServerId
			,@RAMUsage
			,@CPUUsage
			,@DiskUsage
	FROM [dbo].[Server] a
	WHERE a.[Server] = @server;

	if (@@ROWCOUNT=0)
		INSERT INTO [dbo].[Server](Server)
		VALUES (@server)

	UPDATE [dbo].[Server] 
	Set [Uptime] = @Uptime
	WHERE [Server] = @server;

RETURN 0
