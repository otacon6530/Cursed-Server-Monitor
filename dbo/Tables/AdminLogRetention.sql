CREATE TABLE [dbo].[AdminLogRetention]
(
	[AdminLogRetentionId] INT NOT NULL CONSTRAINT PK_AdminLogRetention_AdminLogRetentionID PRIMARY KEY identity(1,1),
	[TableName] VARCHAR(100) NOT NUlL,
	[DaysRetained] INT NOT NULL
)
