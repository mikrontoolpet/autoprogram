from pathlib import Path
from autoprogram.tools.common import Tool
from autoprogram.wbhandler import WorkBook
from autoprogram import config

class Titanium(Tool):
    family_address = "drills/drills/Titanium" # must be equal to the relative path with respect to the master program 

    def __init__(self, name, diam, fl_len, lead):
        super().__init__(name, Titanium.family_address)
        self.diam = diam
        self.fl_len = fl_len
        self.lead = lead

        # Input parameters constraints
        if self.diam < 0.95 or self.diam > 4:
            raise ValueError(f"The input diameter is out of boundary: {self.diam}")
        if self.fl_len < 6*diam or self.fl_len > 20*self.diam:
            raise ValueError(f"The input flute length is out of boundary: {self.fl_len}")

    async def set_parameters(self):
        Set 1
        Set Common Data
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", 140)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/Ta0", -0.143)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", 3.4*self.diam)

        # Set parameters
        # Flute 1
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", self.fl_len)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)
        # Flute 1 (G1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Core Diameter", "34%;31%")
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Rake Angle", 18)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Circular Land Width", 0.8*self.diam)
        # Flute 101 (SGR. G1)
        fl_stk_rmv = 0.02*self.diam
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", -fl_stk_rmv)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Core Diameter", "38%;35%")
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Angle", 18)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Circular Land Width", 0.8*self.diam + 2*fl_stk_rmv)
        #Flute 1001 (G2)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Connection Point", "s0;91.5%")
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute Length", self.fl_len)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", self.lead)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Core Diameter", 55)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Rake Angle", 1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Circular Land Width", 1.09*self.diam)

        # Step 0
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Index", 0)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Chisel Distance", 0.089*self.diam)

        # Gash (TN1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Rotation", -4.5)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", 0.12*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Angle", 64)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Rake Angle", 10)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Depth Past Center Yp", -0.22*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Angle", 90)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Length", 0.015*self.diam)

        # S-Gash (SS)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Gash Rotation", 30)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Web Thickness", -0.009*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Gash Angle", 58)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Rake Angle", -0.5)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Depth Past Center Yp", -0.053*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.17*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Exit Angle Correction", 4)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Chisel Distance Correction", -0.002*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sR", 0.086*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sA", 58)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sL", 0.25*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Exit Angle", 5)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Walk Coefficient", 30)

        # Point Relief
        # Relief 1
        # Point Relief 1 (P1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Relief Angle", 13)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL Start", 0.1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL End", 0.1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Direction of Grinding Marks", 0)
        # Point Relief 2 (P2)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Relief Angle", 30)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL Start", 0.1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL End", 0.1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Direction of Grinding Marks", 0)
        # Relief 101
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Stock Removal", 0.05)
        # Point Relief 102 (SGR P2)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Relief Angle", 30)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL Start", 0.1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL End", 0.1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Direction of Grinding Marks", 0)

        # Step 0 Diameter
        # Step 0 OD Clearance
        # OD Clearance 1 (F1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Margin Width", 0.07*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Back Clearance", 95)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Setting Angle", 45)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Drop Angle", 1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/C Rotation at end", 70)
        # OD Clearance 101 (F2)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Margin Width", 0.22*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Back Clearance", 95)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Setting Angle", 45)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Drop Angle", 1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/C Rotation at end", 0)
        # OD Clearance 201 (F3)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Margin Width", 0.63*self.diam)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Back Clearance", 95)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Setting Angle", 45)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Drop Angle", 1)
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/C Rotation at end", 0)

        # Set 2
        # Reliefs
        # Relief Section 2
        # Relief 1
        # Cam 1
        await self.vgp.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Start Angle C", 20)
        await self.vgp.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Rotation C", 30)
        await self.vgp.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Exit distance", 0.3)

        # Blank
        await self.vgp.set("ns=2;s=ns=2;s=tool/Blank/Profile/D", self.diam)
        await self.vgp.set("ns=2;s=tool/Blank/Profile/L", self.fl_len + 0.5*self.diam)

    async def set_wheels(self):
        # Load wheelpacks
        whp_name = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "whp_posn_6")
        whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
        await self.vgp.load_wheel(whp_path, 5)

        # Set wheel segments
        op_wh_seg = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("wheels", "diam", self.diam, "G1")
        await self.vgp.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)
