# Generated prediction_script.R
system("Rcmd.exe INSTALL --preclean --no-multiarch --with-keep.source prediction15")

library(prediction15)

# 3. 폴더 생성
dir.create("Temp", showWarnings = FALSE)
dir.create("Results", showWarnings = FALSE)

# 4. Database 환경설정
Sys.setenv("DATABASECONNECTOR_JAR_FOLDER" = "C:/Users/ljh86/Desktop/rServer/uploads/teeeeest74564465")
outputFolder <- "C:/Users/ljh86/Desktop/rServer/uploads/teeeeest74564465/Results"
dbms <- "postgresql" #변경 불필요
user <- "iteyes" #변경 필요
pw <- "iteyes" #변경 필요
server <- '61.97.184.196/cdm_bsh' #변경 필요
port <- '5432' #변경 불필요
connectionDetails <- DatabaseConnector::createConnectionDetails(
    dbms = dbms,
    server = server,
    user = user,
    password = pw,
    port = port
)
cdmDatabaseSchema <- "cdm"
cdmDatabaseName <- "cdm_bsh"
cohortDatabaseSchema <- "webapi"
cohortTable <- "prediction15"
cohortTableOutcome <- "prediction15Outcome"
databaseId <- "webapi"
databaseName <- "cdm_bsh"
databaseDescription <- "pusan national university hospital"
oracleTempSchema <- NULL

databaseDetails <- PatientLevelPrediction::createDatabaseDetails(
    connectionDetails = connectionDetails,
    cdmDatabaseSchema = cdmDatabaseSchema,
    cdmDatabaseName = cdmDatabaseName,
    tempEmulationSchema = cdmDatabaseSchema,
    cohortDatabaseSchema = cdmDatabaseSchema,
    cohortTable = cohortTable,
    outcomeDatabaseSchema = cdmDatabaseSchema,
    outcomeTable = cohortTable,
    cohortId = NULL,
    outcomeIds = NULL,
    cdmVersion = 5
)

logSettings <- PatientLevelPrediction::createLogSettings(
    verbosity = "INFO",
    timeStamp = T,
    logName = 'skeletonPlp'
)

# 5. Prediction 실행
createProtocol <- TRUE
createCohorts <- TRUE
runDiagnostic <- FALSE
viewDiagnostic <- FALSE
runAnalyses <- TRUE
createValidationPackage <- FALSE
analysesToValidate = NULL
packageResults <- FALSE
minCellCount = 5
createShiny <- TRUE
sampleSize <- 1000

execute(
    databaseDetails = databaseDetails,
    outputFolder = outputFolder,
    createProtocol = createProtocol,
    createCohorts = createCohorts,
    runDiagnostic = runDiagnostic,
    viewDiagnostic = viewDiagnostic,
    runAnalyses = runAnalyses,
    createValidationPackage = createValidationPackage,
    analysesToValidate = analysesToValidate,
    packageResults = packageResults,
    minCellCount = minCellCount,
    logSettings = logSettings,
    viewShiny = T,
    sampleSize = sampleSize
)

# 샤이니 생성
PatientLevelPrediction::viewMultiplePlp(outputFolder)
