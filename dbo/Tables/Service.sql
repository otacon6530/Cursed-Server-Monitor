CREATE TABLE [dbo].[Service]
(
	[ServiceId] INT NOT NULL CONSTRAINT pk_Service_ServiceId PRIMARY KEY identity(1,1),
	[ServerId] INT NOT NULL CONSTRAINT fk_Service_ServerId FOREIGN KEY REFERENCES [dbo].[Server](ServerId),
	[Service] VARCHAR(100) NOT NULL
)
