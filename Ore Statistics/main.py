import anvil, math
from matplotlib import pyplot as plt

# Isaiah Harville 

#|=-=-=-=|#
# Each region is 32x32 chunks
# In r.0.0 you have 1024 chunks including xyz (0, 0, 0)
# One chunk is 16x16 so each region consists of 262144 blocks -- equated by (region dimensions) * (chunk dimensions) = n (blocks)
#|=-=-=-=|#

# Dictionary containing the block objects and the occurences of each.
blockObjects = {
                anvil.Block('mineraft', 'diamond_ore').id : 0,
                anvil.Block('minecraft', 'gold_ore').id : 0,
                anvil.Block('minecraft', 'iron_ore').id : 0,
                anvil.Block('minecraft', 'coal_ore').id : 0
                }

# Set the region from the folder
region = anvil.Region.from_file('region/r.0.0.mca')


# Data Generation
for i in range(32): # X range of a region
    for j in range(32): # Y range of a region
        try:
            chunk = anvil.Chunk.from_region(region, i, j) # Getting chunks of region (0,0)

            for y in range(70): # Y range for a chunk w/ caves
                for x in range(16): # X range for a chunk
                    for z in range(16): # Z range for a chunk
                        block = chunk.get_block(x,y,z)
                        
                        if block.id in blockObjects:
                            blockObjects[block.id] += 1
                            
                            chunk_x = i * 16 + x
                            chunk_z = j * 16 + z
                            
                            #print('%s located at (%g, %g, %g)'%(block.id, chunk_x, y, chunk_z))

        except anvil.errors.ChunkNotFound: 
            pass # Not all of a region's chunks are saved to the file. They are loaded as they are discovered.
                 # If a chunk hasn't been discovered then it doesn't exist in the save file.


# Math Plotting
plt.axis("equal")
plt.pie([int(blockObjects[i]*100) for i in blockObjects], labels=['Diamond', 'Gold', 'Iron', 'Coal'], autopct='%1.1f%%')
plt.legend(loc='lower right')
plt.title('Percentage of Ore found in a Region')
plt.show()