CREATE PROCEDURE [dbo].[GetServerMetrics]
	@server VARCHAR(100)
AS
	SELECT Top 1 b.[RAMUsage],
		   b.[CPUUsage],
	       b.[DiskUsage],
		   a.[Uptime]
	FROM [dbo].[Server] a
		INNER JOIN [log].[Server] b 
			ON a.[ServerId] = b.[ServerId]
	WHERE a.[Server] = @server
	ORDER BY [InsertDate] DESC;
RETURN 0
