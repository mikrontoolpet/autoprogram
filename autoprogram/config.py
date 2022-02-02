from pathlib import Path

class Config(object):
	MASTER_PROGS_BASE_DIR = "V:/Common/MTI_Production-Engineering-Team/AUTOPROGRAM/master_progs_base_dir"
	RES_PROGS_DIR = "C:/RES"
	WHILE_WAIT_PERIOD = 1.2 # seconds
	APP_STATE_SUB_PERIOD = 100 # milliseconds
	STD_WHP_BASE_DIR = "V:/MTO/Common/Articoli_Mikron_Tool_International/Wheel_Packs/PWS_R628XW/Create"	
	CUST_WHP_BASE_DIR = "V:/MTO/Common/Articoli_Mikron_Tool_International/Wheel_Packs/PWI_R628XW/Create"
	WHP_SUFFIX = ".whs"
	VGP_SUFFIX = ".vgp"
	ISOEASY_SUFFIX = ".vgpx"
	SERVER_URL = "opc.tcp://localhost:8996/"
	MASTER_PROG_DIR = "master_programs"
	COMMON_FILE_DIR = "common"
	ISOEASY_DIR = "isoeasy"
	WORKSHEETS_DIR = "worksheets"
	CONFIG_FILE_NAME = "configuration_file.xlsx"
	COMMON_FILE_NAME = "common.xlsx"
	MASTER_PROG_NAME = "master_program"
	ADD_CHARS = "[°¦m¦mm¦s¦/¦min¦%¦ ]"
	CREATE_WHP_SUFFIX = " Create"
	COMMON_WB_PATH = Path(MASTER_PROGS_BASE_DIR).joinpath(COMMON_FILE_DIR, COMMON_FILE_NAME)