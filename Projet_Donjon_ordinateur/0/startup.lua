require "command_api"


local origin_pos = {0,0,0}
local file = fs.open("file.json", "r")
local contents = file.readAll()
file.close()

data = textutils.unserialiseJSON(contents)

for var=0,35 do
    commands.exec("/fill -20 " .. var-2 .. " " .. -20 .. " " .. 150 .. " " .. var-2 .. " " .. 150 .. " air replace")
end
print("Done")
read()
local file = fs.open("out.txt", "w")
for k in pairs(data) do 
    file.write(spawnStructure(data[k]["filename"] , data[k]["position"] , data[k]["rotation"] , data[k]["mirror"],origin_pos) .. "\n")
end
file.close()