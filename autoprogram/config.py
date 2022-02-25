from pathlib import Path

class Config(object):
	MASTER_PROGS_BASE_DIR = r"\\mikron.net\Group\MT\Common\MTI_Production-Engineering-Team\AUTOPROGRAM\master_progs_base_dir"
	RES_PROGS_DIR = "C:/RES"
	WHILE_WAIT_PERIOD = 1.2 # seconds
	APP_STATE_SUB_PERIOD = 100 # milliseconds
	STD_WHP_BASE_DIR = r"\\mikron.net\Group\MT\MTO\Common\Articoli_Mikron_Tool_International\Wheel_Packs\PWS_R628XW\Create"	
	CUST_WHP_BASE_DIR = r"\\mikron.net\Group\MT\MTO\Common\Articoli_Mikron_Tool_International\Wheel_Packs\PWI_R628XW\Create"
	WHP_SUFFIX = ".whs"
	VGP_SUFFIX = ".vgp"
	ISOEASY_SUFFIX = ".vgpx"
	SERVER_URL = "opc.tcp://localhost:8996/"
	MASTER_PROG_DIR = "master_programs"
	COMMON_FILE_DIR = "common"
	ISOEASY_DIR = "isoeasy"
	WORKSHEETS_DIR = "worksheets"
	CONFIG_FILE_NAME = "configuration_file.xlsx"
	CREATE_FILE_NAME = "create_file.xlsx"
	COMMON_FILE_NAME = "common.xlsx"
	MASTER_PROG_NAME = "master_program"
	ADD_CHARS = "[°¦m¦mm¦s¦/¦min¦%¦ ]"
	CREATE_WHP_SUFFIX = " Create"
	COMMON_WB_PATH = Path(MASTER_PROGS_BASE_DIR).joinpath(COMMON_FILE_DIR, COMMON_FILE_NAME)
	VGPRO_EXE_PATH = "C:/Program Files (x86)/ROLLOMATIC/VirtualGrindPro/1.34.3/bin/VirtualGrindPro.exe"
	R628XW_ID = "R628XW"
	R628XW_ARG = "../MachinesRes/Machines/Cnc628xw/v7.0.37.0/cnc628xw.rds"
	MACHINE_ARG_DICT = {}
	MACHINE_ARG_DICT[R628XW_ID] = R628XW_ARG
	MODES = ["Manual", "Auto"]