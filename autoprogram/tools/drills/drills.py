import asyncio
from autoprogram import config
from autoprogram.vgpclient import VgpClient
from autoprogram.wbhandler import WorkBook

class Titanium:
    family_address = "drills/drills/Titanium" # must be equal to the relative path with respect to the master program 

    def __init__(self, diam, fl_len, lead):
        self.diam = diam
        self.fl_len = fl_len
        self.lead = lead

        # Input parameters constraints
        if self.diam < 0.95 or self.diam > 4:
            raise ValueError(f"The input diameter is out of boundary: {self.diam}")
        if self.fl_len < 6*diam or self.fl_len > 20*self.diam:
            raise ValueError(f"The input flute length is out of boundary: {self.fl_len}")

    async def set_parameters(self, vgpc):
        """
        Set parameters method, common to all the tool classes
        """

        # Set 1
        # Set Common Data
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", 140)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/Ta0", -0.143)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", 3.4*self.diam)

        # Set parameters
        # Flute 1
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", self.fl_len)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)
        # Flute 1 (G1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Core Diameter", "34%;31%")
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Rake Angle", 18)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Circular Land Width", 0.8*self.diam)
        # Flute 101 (SGR. G1)
        fl_stk_rmv = 0.02*self.diam
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", -fl_stk_rmv)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Core Diameter", "38%;35%")
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Angle", 18)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Circular Land Width", 0.8*self.diam + 2*fl_stk_rmv)
        #Flute 1001 (G2)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Connection Point", "s0;91.5%")
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute Length", self.fl_len)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", self.lead)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Core Diameter", 55)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Rake Angle", 1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Circular Land Width", 1.09*self.diam)

        # Step 0
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Index", 0)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Chisel Distance", 0.089*self.diam)
        # Gash (TN1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Rotation", -4.5)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", 0.12*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Angle", 64)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Rake Angle", 10)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Depth Past Center Yp", -0.22*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Angle", 90)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Length", 0.015*self.diam)

        # S-Gash (SS)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Gash Rotation", 30)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", -0.009*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Gash Angle", 58)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Rake Angle", -0.5)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Depth Past Center Yp", -0.053*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.17*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Exit Angle Correction", 4)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Chisel Distance Correction", -0.002*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sR", 0.086*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sA", 62.5)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sL", 0.25*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Exit Angle", 5)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Walk Coefficient", 30)

        # Point Relief
        # Relief 1
        # Point Relief 1 (P1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Relief Angle", 13)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL Start", 0.1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL End", 0.1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Direction of Grinding Marks", 0)
        # Point Relief 2 (P2)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Relief Angle", 30)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL Start", 0.1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL End", 0.1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Direction of Grinding Marks", 0)
        # Relief 101
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Stock Removal", 0.05)
        # Point Relief 102 (SGR P2)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Relief Angle", 30)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL Start", 0.1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL End", 0.1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Direction of Grinding Marks", 0)

        # Step 0 Diameter
        # Step 0 OD Clearance
        # OD Clearance 1 (F1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Margin Width", 0.07*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Back Clearance", 95)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Setting Angle", 45)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Drop Angle", 1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/C Rotation at end", 70)
        # OD Clearance 101 (F2)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Margin Width", 0.22*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Back Clearance", 95)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Setting Angle", 45)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Drop Angle", 1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/C Rotation at end", 0)
        # OD Clearance 201 (F3)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Margin Width", 0.63*self.diam)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Back Clearance", 95)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Setting Angle", 45)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Drop Angle", 1)
        await vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/C Rotation at end", 0)

        # Set 2
        # Reliefs
        # Relief Section 2
        # Relief 1
        # Cam 1
        await vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Start Angle C", 20)
        await vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Rotation C", 30)
        await vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Exit distance", 0.3)

        # Blank
        await vgpc.set("ns=2;s=ns=2;s=tool/Blank/Profile/D", self.diam)
        await vgpc.set("ns=2;s=tool/Blank/Profile/L", self.fl_len + 0.5*self.diam)
            
            # Eventually save the program on the local machine and close it, after
            # all the parameters have been changed
            #await vgpc.save_tool(res_prog_path)
            #await vgpc.close_file()

    async def create(self, name):
        # Get the correct master program path
        master_prog_name = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/drills/drills/Titanium/configuration_file.xlsx").lookup("Foglio1", "diam", self.diam, "master_prog_name")
        master_prog_path = config.MASTER_PROGS_BASE_DIR + "/" + Titanium.family_address + "/" + master_prog_name

        # Set the result program path
        res_prog_path = config.RES_PROGS_DIR + "/" + name + ".vgp"
        # Connect to server
        async with VgpClient("opc.tcp://localhost:8996/") as vgpc:
            # Load the correct master program and save on the local machine
            await vgpc.load_tool(master_prog_path)
            task = asyncio.create_task(self.set_parameters(vgpc))
            done, pending = await asyncio.wait({task})

            # if task in done:
            #     await vgpc.save_tool(res_prog_path)
            #     await vgpc.close_file()