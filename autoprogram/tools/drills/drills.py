from pathlib import Path
from autoprogram.tools.common import Tool
from autoprogram.wbhandler import WorkBook
from autoprogram import config

class Titanium(Tool):
    """
    Titanium drill class
    """
    """
    The class variable "family_address" is necessary and must be equal
    to both:
    1) The relative path between the master programs base directory and the
       master program directory itself
    2) The relative module path between the module "tools" and this class
    """
    family_address = "drills/drills/Titanium"

    def __init__(self, vgp_client, name, diam, fl_len, lead):
        super().__init__(vgp_client, name, Titanium.family_address)
        self.diam = float(diam)
        self.fl_len = float(fl_len)
        self.lead = float(lead)

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1, 6.35)
        self.check_boundary(self.fl_len, 6*self.diam, 20*self.diam)

    async def set_parameters(self):
        # Common data
        fl_rad_stk_rmv = 0.05 # radial stock removal for fluting
        point_stk_rmv = 0.05 # radial stock removal for the point

        # Margin calculations
        circ_land_width = 0.6*self.diam
        land_width_1 = 0.07*self.diam
        land_width_2 = 0.07*self.diam
        f_wh_width = float(WorkBook("C:/Users/0gugale/Desktop/master_progs_base_dir/drills/drills/Titanium/configuration_file.xlsx").lookup("whp_4", "diam", self.diam, "f_wh_width")) # formatted as float to make calculations
        rel_width = circ_land_width - land_width_1 - land_width_2
        marg_width_1 = land_width_1 # program parameter to create the first land width
        marg_width_101 = marg_width_1 + rel_width - f_wh_width # program parameter to create the second land width

        # # Set 1
        # # Set Common Data
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", 140)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/Ta0", -0.143)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", 3.4*self.diam)

        # Set parameters
        # Flute 1
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", self.fl_len)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)
        # Flute 1 (G1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Core Diameter", "34%;31%")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Rake Angle", 18)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Circular Land Width", circ_land_width)
        # Flute 101 (SGR. G1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", -fl_rad_stk_rmv)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Core Diameter", "38%;35%")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Angle", 18)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Circular Land Width", circ_land_width + 2*fl_rad_stk_rmv)
        #Flute 1001 (G2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Connection Point", "s0;91.5%")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute Length", self.fl_len)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", self.lead)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Core Diameter", 55)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Rake Angle", 1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Circular Land Width", 1.09*self.diam)
        s_g1_feedrate = WorkBook("C:/Users/0gugale/Desktop/master_progs_base_dir/drills/drills/Titanium/configuration_file.xlsx").lookup("parameters", "diam", self.diam, "S_G1 Feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", s_g1_feedrate)
        s_g1_feedrate_in = WorkBook("C:/Users/0gugale/Desktop/master_progs_base_dir/drills/drills/Titanium/configuration_file.xlsx").lookup("parameters", "diam", self.diam, "S_G1 Feedrate In")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate In", s_g1_feedrate_in)
        res = await self.vgpc.get("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0")

        # # Step 0
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Index", 0)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Chisel Distance", 0.089*self.diam)

        # # Gash (TN1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Rotation", -4.5)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", 0.12*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Angle", 64)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Rake Angle", 10)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Depth Past Center Yp", -0.22*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Angle", 90)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Length", 0.015*self.diam)

        # # S-Gash (SS)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Gash Rotation", 30)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Web Thickness", -0.009*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Gash Angle", 58)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Rake Angle", -0.5)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Depth Past Center Yp", -0.053*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.17*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Exit Angle Correction", 4)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Chisel Distance Correction", -0.002*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sR", 0.086*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sA", 58)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sL", 0.25*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Exit Angle", 5)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Walk Coefficient", 30)

        # # Point Relief
        # # Relief 1
        # # Point Relief 1 (P1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Relief Angle", 13)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL Start", 0.1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL End", 0.1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Direction of Grinding Marks", 0)
        # # Point Relief 2 (P2)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Relief Angle", 30)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL Start", 0.1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL End", 0.1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Direction of Grinding Marks", 0)
        # # Relief 101
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Stock Removal", 0.05)
        # # Point Relief 102 (SGR P2)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Relief Angle", 30)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL Start", 0.1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL End", 0.1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Direction of Grinding Marks", 0)

        # # Step 0 Diameter
        # # Step 0 OD Clearance
        # # OD Clearance 1 (F1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Margin Width", marg_width_1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Back Clearance", 95)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Setting Angle", 45)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Drop Angle", 1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/C Rotation at end", 70)
        # # OD Clearance 101 (F2)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Margin Width", 0.22*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Back Clearance", 95)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Setting Angle", 45)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Drop Angle", 1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/C Rotation at end", 0)
        # # OD Clearance 201 (F3)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Margin Width", 0.63*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Back Clearance", 95)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Setting Angle", 45)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Drop Angle", 1)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/C Rotation at end", 0)

        # # Set 2
        # # Reliefs
        # # Relief Section 2
        # # Relief 1
        # # Cam 1
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Start Angle C", 20)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Rotation C", 30)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Exit distance", 0.3)

        # # Blank
        # await self.vgpc.set("ns=2;s=ns=2;s=tool/Blank/Profile/D", self.diam)
        # await self.vgpc.set("ns=2;s=tool/Blank/Profile/L", self.fl_len + 0.5*self.diam)

    async def set_wheels(self):
        pass
        # whp_path = "C:\\Users\\0gugale\\Desktop\\PWS_509_MTI Create.whs"
        # await self.vgpc.load_wheel(whp_path, 1)
        # whp_path = "C:\\Users\\0gugale\\Desktop\\PWS_554_MTI Create.whs"
        # await self.vgpc.load_wheel(whp_path, 2)
        # whp_path = "C:\\Users\\0gugale\\Desktop\\PWS_563_MTI Create.whs"
        # await self.vgpc.load_wheel(whp_path, 3)

        # # Load wheelpacks and set wheel segments
        # # Load wheelpack 1
        # whp_name = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "whp_posn_1")
        # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
        # await self.vgpc.load_wheel(whp_path, 1)
        # # Set wheel segments for wheelpack 1
        # # S_G1
        # op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "S_G1")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)

        # # Load wheelpack 2
        # whp_name = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "whp_posn_2")
        # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
        # await self.vgpc.load_wheel(whp_path, 2)
        # # Set wheel segments for wheelpack 2
        # # TN1
        # op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "TN1")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Wheel", op_wh_seg)
        # # SS
        # op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "TN1")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Wheel", op_wh_seg)
        # # P1
        # op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "P1")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)
        # # P2
        # op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "P2")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)
        # # S_P2
        # op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "S_P2")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)

        # # Load wheelpack 4
        # whp_name = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "whp_posn_4")
        # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
        # await self.vgpc.load_wheel(whp_path, 4)
        # # Set wheel segments for wheelpack 4
        # # F1
        # op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "S_P2")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)

        # # Load wheelpack 5
        # whp_name = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "whp_posn_5")
        # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
        # await self.vgpc.load_wheel(whp_path, 5)
        # # Set wheel segments for wheelpack 5
        # pass
        
        # # Load wheelpack 6
        # whp_name = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "whp_posn_6")
        # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
        # await self.vgpc.load_wheel(whp_path, 6)
        # # Set wheel segments for wheelpack 6
        # # G1
        # op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "G1")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)
        # # G2
        # op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "G2")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Wheel", op_wh_seg)