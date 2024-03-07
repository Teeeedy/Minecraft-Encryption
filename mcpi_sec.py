from mcpi.minecraft import Minecraft

# Assignment 3 main file
# Feel free to modify, and/or to add other modules/classes in this or other files
#"localhost", 4712
mc = Minecraft.create("localhost", 4712)
mc.postToChat("bbb")
block = mc.getBlock(0,0,0)
print(block)