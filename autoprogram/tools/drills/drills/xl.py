from pathlib import Path
import math
from autoprogram.tools.basetool import BaseTool
from autoprogram.wbhandler import WorkBook


class Tool(BaseTool):
    """
    CrazyDrill XL 
    """
    """
    The class variable "family_address" is necessary and must be equal
    to both:
    1) The relative path between the master programs base directory and the
       master program directory itself
    2) The relative module path between the module "tools" and this class
    """
    family_address = "drills/drills/xl"
    machine = "R628XW"

    def __init__(self, vgp_client, name, diameter):
        super().__init__(vgp_client, name) # update class name here too!
        self.diam = float(diameter)

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1.4, 6.4)

    async def set_parameters(self):

        end_stk_rmv = self.common_wb.lookup("end_stock", "diameter", self.diam, "end_stock")

        #blank
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/D", self.diam)
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/L", self.diam*11)

        # Set parameters
        # Set 1
        # Common Data
        d700 = self.common_wb.lookup("D700", "diameter", self.diam, "D700")
        await self.vgpc.set("ns=2;s=tool/Tool/Reference Length (RL)", 0.75*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/End Stock Removal (dL)", end_stk_rmv)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Cutting Security Distance", d700)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Cutting Security Distance", d700)

        # Set 1
        # Profile
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", self.diam)

        #  # Flute 1 (G1)
        lead = self.configuration_wb.lookup("blank", "diameter", self.diam, "lead")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", lead)
        G1_attack_angle = self.configuration_wb.trend("function_data", "diameter", self.diam, "G1_attack_angle")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Attack Angle", G1_attack_angle)

        #  # Flute 1001 (G2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", lead)
        G2_attack_angle = self.configuration_wb.trend("function_data", "diameter", self.diam, "G2_attack_angle")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Attack Angle", G2_attack_angle)

        # S-Gash
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.225*self.diam)

        # TN1
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", 0.153*self.diam)

        # Set 2
        # Profile
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Diameter", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Distance", 0.286*self.diam)

        # TN2
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/D", 1.17*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/dD", 0.943*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/dZ", -(0.168*self.diam))
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Web Thickness", 0.04*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Profile 2D/sR", 0.323*self.diam)


    async def set_wheels(self):
        """
        Load wheelpacks and set wheel segments
        """
        # Load wheelpack 1
        whp_name = self.configuration_wb.lookup("wheelpacks", "diameter", self.diam, "wheelpack_1")
        await self.load_wheel(whp_name, 1)
        # Load wheelpack 2
        whp_name = self.configuration_wb.lookup("wheelpacks", "diameter", self.diam, "wheelpack_2")
        await self.load_wheel(whp_name, 2)
        # # Skip wheelpack 3
        # # Load wheelpack 4
        # whp_name = self.configuration_wb.lookup("wheelpack_4", "diameter", self.diam, "wheelpack_4")
        # await self.load_wheel(whp_name, 4)
        # # Load wheelpack 5
        # whp_name = self.configuration_wb.lookup("wheelpack_5", "diameter", self.diam, "wheelpack_5")
        # await self.load_wheel(whp_name, 5)
        # Load wheelpack 6
        whp_name = self.configuration_wb.lookup("wheelpacks", "diameter", self.diam, "wheelpack_6")
        await self.load_wheel(whp_name, 6)

        # # Set wheel segments for wheelpack 1
        # # G1
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Wheel", op_wh_seg)
        

        # # Set wheel segments for wheelpack 2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("SM", "diameter", self.diam, "SM_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Wheel", op_wh_seg)

        # # Set wheel segments for wheelpack 4

        # # Set wheel segments for wheelpack 5

        # # Set wheel segments for wheelpack 6
        # G1
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Wheel", op_wh_seg)
        # G2
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Wheel", op_wh_seg)
        

    async def set_isoeasy(self):
        """
        Load specified isoeasy program
        """
        # isoeasy_name = self.configuration_wb.lookup("isoeasy", "diameter", self.diam, "isoeasy_name")
        # isoeasy_path = self.full_isoeasy_path(isoeasy_name)
        # await self.vgpc.load_isoeasy(isoeasy_path)
        pass

    def set_datasheet(self):
        """
        Write additional information on datasheet
        """
        # if (self.fl_len/self.diam - 3) <= 6:
        #     support_len = self.configuration_wb.lookup("datasheet", "diameter", self.diam, "support_len_6xd")
        # else:
        #     support_len = self.configuration_wb.lookup("datasheet", "diameter", self.diam, "support_len_10xd")

        # support_len_text = "Support length: " + str(support_len) + " mm"
        # self.datasheet_args.append(support_len_text)
        pass