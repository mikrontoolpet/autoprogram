from pathlib import Path
import math
from autoprogram.tools.common import BaseTool
from autoprogram.wbhandler import WorkBook

class Tool(BaseTool):
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
    family_address = "drills/drills/ic"

    def __init__(self, vgp_client, name, diam, fl_len, lead):
        super().__init__(vgp_client, name, Tool.family_address) # update class name here too!
        self.diam = float(diam)
        self.fl_len = float(fl_len)
        self.lead = float(lead)
        self.configuration_wb = WorkBook("V:/Common/MTI_Production-Engineering-Team/VGPro_Master_Programs/master_progs_base_dir/drills/drills/ic/configuration_file.xlsx")

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1, 6.35)
        self.check_boundary(self.fl_len, 6*self.diam, 25*self.diam)

    async def set_parameters(self):
        # Margin calculations
        # Circular land width varies along the flute length
        # land_width_1 = 0.07*self.diam
        # land_width_2 = 0.07*self.diam
        # f_wh_width = float(WorkBook("C:/Users/0gugale/Desktop/master_progs_base_dir/drills/drills/Titanium/configuration_file.xlsx").lookup("whp_4", "diam", self.diam, "f_wh_width")) # formatted as float to make calculations
        # rel_width = circ_land_width - land_width_1 - land_width_2
        # marg_width_1 = land_width_1 # program parameter to create the first land width
        # marg_width_101 = marg_width_1 + rel_width - f_wh_width # program parameter to create the second land width

        # Set parameters
        # Set 1
        # Common Data
        await self.vgpc.set("ns=2;s=tool/Tool/Reference Length (RL)", 1.5*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/End Stock Removal (dL)", 0.0579*self.diam + 0.0342)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Cutting Security Distance", 0.1685*self.diam + 0.1331)
        # delta_dl = await self.vgpc.get("ns=2;s=tool/Tool/Set 1/Delta dL (Output)")

        # Profile
        point_ang = 141
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", point_ang)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/Ta0", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", 5.3*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Straightness Diameter", 1)
        # point_len = self.diam/2*math.tan(math.radians(90 - point_ang/2))

        # Flute 1
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Index", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", 6.3*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Z Position", 0)

        # Flute 1 (G1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Core Diameter", 30) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Attack Angle", 0.5)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL End", -1.8*self.diam)
        # Feeds and speeds
        # g1_speed = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G1_speed")
        # g1_feedrate = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G1_feedrate")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Cutting Speed", g1_speed)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g1_feedrate)

        # Flute 101 (G2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", 0.02143*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Core Diameter", 54) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Attack Angle", 7.5)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL Start", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL End", 0)
        # Feeds and speeds
        # g2_speed = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G2_speed")
        # g2_feedrate = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G2_feedrate")
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Cutting Speed", g2_speed)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate", g2_feedrate)

        # Flute 201 (S_G1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Rake Shift", -0.01429*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Core Diameter", 35) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Attack Angle", 10)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL Start", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL End", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Infeed Down Y", 0.07143*self.diam)
       # Feeds and speeds
        # MISSING DATA!!!

        # Flute 1001
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Connection Point", "s1;60%")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Delta Index for Connexion Point", -0.5)
        # Custom Profile Flute
        g3_x_eot_offset = -4.1571*self.diam
        fl_len_diff = 0.2714*self.diam
        g3_len = self.fl_len + g3_x_eot_offset - fl_len_diff
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Custom Profile Flute/dZ", -4.1571*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Custom Profile Flute/D", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Custom Profile Flute/L", g3_len)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Custom Profile Flute/Ta", 0)

        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", self.lead)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Z Position", 0)

        # Flute 1001 (G3)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1001 (Output)/Core Diameter", 25) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1001 (Output)/Attack Angle", 7.5)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1001 (Output)/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1001 (Output)/dL Start", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1001 (Output)/dL End", -0.3571*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1001 (Output)/Infeed Down Y", 0.2143*self.diam)
        # Feeds and speeds
        # MISSING DATA!!!

        # Flute 1101 (S_G3)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1101/Rake Shift", -0.01786*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1101/Core Diameter", 30) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1101/Attack Angle", 15)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1101/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1101/dL Start", 0.4286*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1101/dL End", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1101/Infeed Down Y", 0.2143*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1101/Exit Radius", 0.5*self.diam)
        # Feeds and speeds
        # MISSING DATA!!!

        # Flute 1201 (RN1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1201/Rake Shift", 0.025*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1201/Core Diameter", 80) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1201/Attack Angle", 15)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1201/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1201/dL Start", -1.857*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1201/dL End", -1.286*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1201/Infeed Down Y", 0.2143*self.diam)
        # Feeds and speeds
        # MISSING DATA!!!

        # Flute 1301 (RN2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1301/Rake Shift", -0.4857*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1301/Core Diameter", 80) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1301/Attack Angle", 15)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1301/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1301/dL Start", 0.7857*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1301/dL End", -self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1301/Infeed Motion (Start)/Z", 0.01429*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1301/Infeed Motion (Start)/Y", 0.25*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1301/Security Distance (End)", 0.25*self.diam)
        # Feeds and speeds
        # MISSING DATA!!!

        # Flute 1401 (BRUSH)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1401/Rake Shift", 0.05357*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1401/Core Diameter", 15) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1401/Attack Angle", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1401/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1401/dL Start", -3.571*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1401/dL End", 2.143*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute 1401/Infeed Down Y", 0.2143*self.diam)
        # Feeds and speeds
        # MISSING DATA!!!

        # Step 0
        # Gash 1 (S1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Gash Rotation", 24)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Web Thickness", 0.012857*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Gash Angle", 55)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Rake Angle", 2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Depth Past Center Yp", -0.02429*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Profile 2D/sR", 0.0649*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Profile 2D/sA", 111)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Profile 2D/sL", 0.55*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Exit Angle", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Attack Angle", 2)

        # Gash 101 (TN3)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Gash Rotation", 24)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Web Thickness", 0.007857*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Gash Angle", 56)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Rake Angle", -10)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Depth Past Center Yp", -0.03*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Profile 2D/sR", 0.0649*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Profile 2D/sA", 95)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Profile 2D/sL", 0.0786*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Exit Angle", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Attack Angle", 2)

        # Gash 201 (TN1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Gash Rotation", -4.6)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Web Thickness", 0.1071*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Gash Angle", 56)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Rake Angle", -10)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Depth Past Center Yp", -0.2*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Sweep Angle", 90)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Sweep Length", 0.05)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Exit Angle", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Attack Angle", 2)

        # Point Relief
        # Relief 1
        # Point Relief 1 (P1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Relief Angle", 12)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL Start", 0.1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL End", 0.5)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Direction of Grinding Marks", 0)
        # Point Relief 2 (P2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Relief Angle", 25)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL Start", 0.1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL End", 0.5)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Direction of Grinding Marks", 0)
        # Relief 101
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Stock Removal", 0.05)
        # Point Relief 102 (SGR P2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Relief Angle", 25)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL Start", 0.1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL End", 0.5)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Direction of Grinding Marks", 0)

        # Step 0 Diameter
        # Step 0 OD Clearance
        # OD Clearance 1 (F1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Margin Width", 0.0857*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Back Clearance", 94)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Setting Angle", 36)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Drop Angle", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/dL Start", 0.2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/dL End", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/C Rotation at end", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Rotation C axial angle", 0)

        # OD Clearance 101 (F2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Margin Width", 0.2371*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Back Clearance", 94)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Setting Angle", 36)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Drop Angle", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/dL Start", 0.2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/dL End", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/C Rotation at end", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Rotation C axial angle", 0)

        # Set 2
        tn2_diam = 1.428*self.diam
        # OD Profile 2D
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/D", tn2_diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/a0", point_ang/2)
        # Gash 1
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Delta Index for Connexion Point", 17.6)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/D", tn2_diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Web Thickness", -0.20286*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Depth Past Center Yp", -0.37286*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Profile 2D/sR", 0.2426*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Profile 2D/sA", 102)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Profile 2D/sL", 0.1)

        # Set 3
        # OD Profile 2D
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/OD Profile 2D/Diameter", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/OD Profile 2D/Distance", 0.3*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/OD Profile 2D/Angle", 25)

        # Blank
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/D", self.diam)
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/L", self.fl_len + 0.5*self.diam)

    async def set_wheels(self):
        pass
    #     # Load wheelpacks and set wheel segments
    #     # Load wheelpack 1
    #     # whp_name = self.configuration_wb.lookup("whp_1", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 1)
    #     # Set wheel segments for wheelpack 1
    #     # S_G1
    #     op_wh_seg = self.configuration_wb.lookup("whp_1", "diam", self.diam, "S_G1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)
    #     # RN
    #     op_wh_seg = self.configuration_wb.lookup("whp_1", "diam", self.diam, "RN_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Wheel", op_wh_seg)

    #     # Load wheelpack 2
    #     # whp_name = self.configuration_wb.lookup("whp_2", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 2)
    #     # Set wheel segments for wheelpack 2
    #     # TN1
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "TN1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Wheel", op_wh_seg)
    #     # SS
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "SS_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Wheel", op_wh_seg)
    #     # P1
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "P1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)
    #     # P2
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "P2_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)
    #     # S_P2
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "S_P2_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)

    #     # Load wheelpack 4
    #     # whp_name = self.configuration_wb.lookup("whp_4", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 4)
    #     # Set wheel segments for wheelpack 4
    #     # F1
    #     op_wh_seg = self.configuration_wb.lookup("whp_4", "diam", self.diam, "F1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Wheel", op_wh_seg)

    #     # Load wheelpack 5
    #     # whp_name = self.configuration_wb.lookup("whp_5", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 5)
    #     # Set wheel segments for wheelpack 5
    #     # ERF
    #     op_wh_seg = self.configuration_wb.lookup("whp_5", "diam", self.diam, "ERF_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Wheel", op_wh_seg)
    #     # ERT
    #     op_wh_seg = self.configuration_wb.lookup("whp_5", "diam", self.diam, "ERT_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Blank Preparation 1/Peeling Operation/Peeling Operation 1/Wheel", op_wh_seg)
        
    #     # # Load wheelpack 6
    #     # whp_name = self.configuration_wb.lookup("wheels", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 6)
    #     # Set wheel segments for wheelpack 6
    #     # G1
    #     op_wh_seg = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)
    #     # G2
    #     op_wh_seg = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Wheel", op_wh_seg)