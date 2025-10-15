CREATE PROCEDURE [dbo].[SetServerMetrics]
	@server VARCHAR(100),
	@RAMUsage INT,
	@CPUUsage INT,
	@DiskUsage INT,
	@Uptime VARCHAR(100)
AS
	INSERT INTO [log].[Server] ([ServerId], [RAMUsage], [CPUUsage], [DiskUsage])
	SELECT a.ServerId
			,@RAMUsage
			,@CPUUsage
			,@DiskUsage
	FROM [dbo].[Server] a
	WHERE a.[Server] = @server;

	UPDATE [dbo].[Server] 
	Set [Uptime] = @Uptime
	WHERE [Server] = @server;

RETURN 0
