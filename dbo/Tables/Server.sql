CREATE TABLE [dbo].[Server]
(
	[ServerId] INT NOT NULL CONSTRAINT PK_Server_ServerID PRIMARY KEY identity(1,1),
	[Server] VARCHAR(100) NOT NULL,
	[Uptime] VARCHAR(100) NULL,
	[CPUDesc] VARCHAR(100) NULL,
	[GPUDesc] VARCHAR(200) NULL,
	[RAMDesc] VARCHAR(100) NULL,
	[NetworkDesc] VARCHAR(500) NULL,
	[LastModified] DATETIME NULL,
	[Status] AS (CASE WHEN dateadd(s,-8,GETDATE()) < [LastModified] THEN 'Active' ELSE 'Inactive' END) 
)

