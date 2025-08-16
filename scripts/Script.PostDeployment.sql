/*
Post-Deployment Script 
*/

--Populate Admin tables with default values if they don't exist. It is requred that these log tables have a retention policy.

CREATE TABLE #AdminLogRetention (
	[TableName] VARCHAR(100) NOT NUlL,
	[DaysRetained] INT NOT NULL 
);

INSERT INTO #AdminLogRetention(TableName,DaysRetained)
VALUES ('CPU',30)
	  ,('Event',30)
	  ,('Server',30)
	  ,('Service',30);

INSERT INTO [dbo].[AdminLogRetention](TableName,DaysRetained)
SELECT a.TableName, a.DaysRetained
FROM #AdminLogRetention a
	LEFT JOIN [dbo].[AdminLogRetention] b
		ON a.TableName = b.TableName
WHERE b.TableName IS NULL; 


--Initial Creation of Agent Job
IF NOT EXISTS (SELECT 1 FROM msdb.dbo.sysjobs WHERE name = N'ApplyRetentionJob')
BEGIN
    EXEC msdb.dbo.sp_add_job 
        @job_name = N'ApplyRetentionJob',
        @owner_login_name = N'sa';

    EXEC msdb.dbo.sp_add_jobstep 
        @job_name = N'ApplyRetentionJob',
        @step_name = N'Apply Log Retention Policies',
        @subsystem = N'TSQL',
        @command = N'EXEC log.ApplyRetention;',
        @database_name = N'$(DatabaseName)',
        @on_success_action = 1,   -- quit with success
        @on_fail_action = 2;      -- quit with failure

    IF NOT EXISTS (SELECT 1 FROM msdb.dbo.sysschedules WHERE name = N'Daily 2AM')
    BEGIN
        EXEC msdb.dbo.sp_add_schedule 
            @schedule_name = N'Daily 2AM',
            @freq_type = 4,  -- daily
            @freq_interval = 1,
            @active_start_time = 020000;
    END

    EXEC msdb.dbo.sp_attach_schedule 
        @job_name = N'ApplyRetentionJob',
        @schedule_name = N'Daily 2AM';

    EXEC msdb.dbo.sp_add_jobserver 
        @job_name = N'ApplyRetentionJob';
END
