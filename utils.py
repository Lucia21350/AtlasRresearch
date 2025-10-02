import os
import zipfile
import shutil
import subprocess

def prediction_research(zip_file, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    zip_path = os.path.join(target_dir, zip_file.filename)
    zip_file.save(zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
        # ZIP 안에 루트 폴더 있는지 확인
        root_folders = set(f.filename.split('/')[0] for f in zip_ref.infolist())
        if len(root_folders) == 1 and all(f.startswith(list(root_folders)[0] + '/') for f in zip_ref.namelist()):
            extracted_main_dir = os.path.join(target_dir, list(root_folders)[0])
        else:
            extracted_main_dir = target_dir

    os.remove(zip_path)

    # jar 파일 경로
    jar_source = os.path.join(os.path.dirname(__file__), "postgresql-42.6.0.jar")
    if not os.path.exists(jar_source):
        raise FileNotFoundError(f"JAR not found: {jar_source}")

    # jar 복사
    jar_target = os.path.join(extracted_main_dir, os.path.basename(jar_source))
    shutil.copy(jar_source, jar_target)

    # renv 폴더 삭제
    renv_folder = os.path.join(extracted_main_dir, "renv")
    if os.path.exists(renv_folder):
        shutil.rmtree(renv_folder)

    # .Rprofile 내용 삭제
    rprofile_file = os.path.join(extracted_main_dir, ".Rprofile")
    if os.path.exists(rprofile_file):
        with open(rprofile_file, "w", encoding="utf-8") as f:
            f.write("")

    # renv.lock 파일 삭제
    renv_lock_file = os.path.join(extracted_main_dir, "renv.lock")
    if os.path.exists(renv_lock_file):
        os.remove(renv_lock_file)

    # prediction_script 생성
    create_prediction_script(extracted_main_dir)

    # prediction_script.R 실행
    r_script = os.path.join(extracted_main_dir, "prediction_script.R")
    if os.path.exists(r_script):
        try:
            subprocess.run(
            ["Rscript", "--no-init-file", r_script],
            cwd=extracted_main_dir
        )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"R script execution failed: {e}")

    return extracted_main_dir


def find_rproj_name(extracted_dir):
    """
    extracted_dir에서 .Rproj 파일 이름 찾아 반환
    확장자는 제거하고 순수 이름만
    """
    for f in os.listdir(extracted_dir):
        if f.endswith(".Rproj"):
            return os.path.splitext(f)[0]  # 확장자 제거
    return None


def get_current_folder_name(path):
    """
    주어진 경로(path)에서 현재 폴더 이름 반환
    """
    return os.path.basename(os.path.abspath(path))


def generate_pred_script_content(rproj_name, extracted_dir, folder_name):
    """
    prediction_script.R 내용 생성
    """
    # 경로 구분자 Windows/Unix 상관없이 맞춰서 처리
    extracted_dir_r = extracted_dir.replace("\\", "/")  

    content = f'''# Generated prediction_script.R
pkg_path <- "C:/Users/ljh86/Desktop/rServer/uploads/{folder_name}"
system(paste("Rcmd.exe INSTALL --preclean --no-multiarch --with-keep.source", shQuote(pkg_path)))

library({rproj_name})

# 3. 폴더 생성
dir.create("Temp", showWarnings = FALSE)
dir.create("Results", showWarnings = FALSE)

# Temp 폴더를 현재 위치로 고정
temp_path <- "C:/Users/ljh86/Desktop/rServer/uploads/{folder_name}/Temp"
dir.create(temp_path, showWarnings = FALSE)

Sys.setenv(TMPDIR = temp_path, TEMP = temp_path, TMP = temp_path)

# R이 내부에서 쓸 tempdir() 을 강제로 덮어쓰기
assignInNamespace("tempdir", function() temp_path, ns = "base")

# 확인용
print(tempdir())

# 4. Database 환경설정
Sys.setenv("DATABASECONNECTOR_JAR_FOLDER" = "{extracted_dir_r}")
outputFolder <- "{extracted_dir_r}/Results"
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
cohortTable <- "{rproj_name}"
cohortTableOutcome <- "{rproj_name}Outcome"
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
sampleSize <- 3000

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
'''
    return content

def create_prediction_script(extracted_dir):
    os.makedirs(extracted_dir, exist_ok=True)
    
    rproj_name = find_rproj_name(extracted_dir)
    folder_name = get_current_folder_name(extracted_dir)

    if not rproj_name:
        raise FileNotFoundError(f"{extracted_dir} 경로에 .Rproj 파일이 없음")
    
    r_script_path = os.path.join(extracted_dir, "prediction_script.R")
    content = generate_pred_script_content(rproj_name, extracted_dir, folder_name)
    
    with open(r_script_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"prediction_script.R 파일 생성: {r_script_path}")




def estimation_research(zip_file, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    zip_path = os.path.join(target_dir, zip_file.filename)
    zip_file.save(zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
        # ZIP 안에 루트 폴더 있는지 확인
        root_folders = set(f.filename.split('/')[0] for f in zip_ref.infolist())
        if len(root_folders) == 1 and all(f.startswith(list(root_folders)[0] + '/') for f in zip_ref.namelist()):
            extracted_main_dir = os.path.join(target_dir, list(root_folders)[0])
        else:
            extracted_main_dir = target_dir

    os.remove(zip_path)

    # jar 파일 경로
    jar_source = os.path.join(os.path.dirname(__file__), "postgresql-42.6.0.jar")
    if not os.path.exists(jar_source):
        raise FileNotFoundError(f"JAR not found: {jar_source}")

    # jar 복사
    jar_target = os.path.join(extracted_main_dir, os.path.basename(jar_source))
    shutil.copy(jar_source, jar_target)

    # renv 폴더 삭제
    renv_folder = os.path.join(extracted_main_dir, "renv")
    if os.path.exists(renv_folder):
        shutil.rmtree(renv_folder)

    # .Rprofile 내용 삭제
    rprofile_file = os.path.join(extracted_main_dir, ".Rprofile")
    if os.path.exists(rprofile_file):
        with open(rprofile_file, "w", encoding="utf-8") as f:
            f.write("")

    # renv.lock 파일 삭제
    renv_lock_file = os.path.join(extracted_main_dir, "renv.lock")
    if os.path.exists(renv_lock_file):
        os.remove(renv_lock_file)

    # estimation_script 생성
    create_estimation_script(extracted_main_dir)

    # estimation_script.R 실행
    r_script = os.path.join(extracted_main_dir, "estimation_script.R")
    if os.path.exists(r_script):
        try:
            subprocess.run(
                ["Rscript", "--no-init-file", r_script],
                cwd=extracted_main_dir
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"R script execution failed: {e}")

    return extracted_main_dir



def create_estimation_script(extracted_dir):
    os.makedirs(extracted_dir, exist_ok=True)
    
    rproj_name = find_rproj_name(extracted_dir)
    folder_name = get_current_folder_name(extracted_dir)

    if not rproj_name:
        raise FileNotFoundError(f"{extracted_dir} 경로에 .Rproj 파일이 없음")
    
    r_script_path = os.path.join(extracted_dir, "estimation_script.R")
    content = generate_est_script_content(rproj_name, extracted_dir, folder_name)
    
    with open(r_script_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"estimation_script.R 파일 생성: {r_script_path}")


def generate_est_script_content(rproj_name, extracted_dir, folder_name):
    """
    estimation_script.R 내용 생성
    """
    # 경로 구분자 Windows/Unix 상관없이 맞춰서 처리
    extracted_dir_r = extracted_dir.replace("\\", "/")  

    content = f'''# Generated estimation_script.R

'''
    return content