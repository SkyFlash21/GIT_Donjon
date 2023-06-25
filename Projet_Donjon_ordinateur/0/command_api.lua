-- Fonction pour placer une structure à un emplacement donné
function spawnStructure(name,pos,rotation,miror,origin_pos)
    local y, x, z = table.unpack(pos)
    command = "/setblock " .. x+origin_pos[1] .. " " .. y+origin_pos[3] .. " " .. z+origin_pos[2] .. " minecraft:structure_block{mode:\"LOAD\",name:\"" .. name .. "\""

    if miror then
        command = command .. ",mirror:\"LEFT_RIGHT\""
    end

    if rotation ~= 0 then
        if rotation == 3 then
            command = command .. ",rotation:\"COUNTERCLOCKWISE_" .. 90 .. "\""
        else
            command = command .. ",rotation:\"CLOCKWISE_" .. rotation*90 .. "\""
        end
    end

    
    command = command .. "}"
    -- Place le bloc de structure avec le nom spécifié
    commands.exec(command)
    -- Place un bloc de redstone supplémentaire pour déclencher la structure
    -- minecraft:structure_block{mirror: "LEFT_RIGHT", rotation: "NONE", mode: "LOAD", posX: 5, posY: 2, posZ: 3, name: "minecraft:sz"}
    commands.exec("/setblock " .. x+origin_pos[1] .. " " .. y+origin_pos[3]+1 .. " " .. z+origin_pos[2] .. " minecraft:redstone_block")
    return command
end


-- Fonction pour placer une ligne de blocs
local function placeLine(x1, y1, z1, x2, y2, z2, a)
    message = ("["..a.."]Ligne entre " .. x1 .. " " .. y1 .. " " .. z1 .. " et " .. x2 .. " " .. y2 .. " " .. z2)
    commands.exec("/say " .. message)
    local dx = math.abs(x2 - x1)
    local dy = math.abs(y2 - y1)
    local dz = math.abs(z2 - z1)

    local steps = math.max(dx, dy, dz)

    local xIncrement = (x2 - x1) / steps
    local yIncrement = (y2 - y1) / steps
    local zIncrement = (z2 - z1) / steps

    for i = 0, steps do
        local x = math.floor(x1 + xIncrement * i + 0.5)
        local y = math.floor(y1 + yIncrement * i + 0.5)
        local z = math.floor(z1 + zIncrement * i + 0.5)

        -- Place le bloc en utilisant la commande setblock
        commands.exec("/setblock " .. x .. " " .. y .. " " .. z .. " minecraft:stone")
        sleep(0.1)
    end
    commands.exec("/say Fin ".. a)
end

-- Fonction pour dessiner une zone de travail
local function clearAndBuildFrame(x, y, z, deep)
    -- Effacer la zone

    for startY = 1, y/2, 1 do
        local clearCommand = "/fill 0 " .. (startY*2)-1 ..  " 0 " .. x .. " " .. startY*2 .. " " .. z .. " minecraft:air"
        commands.exec(clearCommand)
    end
    if deep then
        -- Construire la structure de blocs en forme de cadre
        local frameCommand = "/fill 0 0 0 " .. x .. " 1 0 minecraft:stone"  -- Fond
        commands.exec(frameCommand)
        frameCommand = "/fill 0 " .. y .. " 0 " .. x .. " " .. y .. " 0 minecraft:stone"  -- Plafond
        commands.exec(frameCommand)
        frameCommand = "/fill 0 0 0 0 " .. y .. " " .. z .. " minecraft:stone"  -- Côté gauche
        commands.exec(frameCommand)
        frameCommand = "/fill " .. x .. " 0 0 " .. x .. " " .. y .. " " .. z .. " minecraft:stone"  -- Côté droit
        commands.exec(frameCommand)
        frameCommand = "/fill 0 0 " .. z .. " " .. x .. " " .. y .. " " .. z .. " minecraft:stone"  -- Côté arrière
        commands.exec(frameCommand)
        frameCommand = "/fill 0 0 0 " .. x .. " " .. y .. " 0 minecraft:stone"  -- Côté avant
        commands.exec(frameCommand)
        frameCommand = "/fill 0 0 0 " .. x .. " 0 ".. z .. " minecraft:stone"  -- Côté bas
        commands.exec(frameCommand)
    end
end

local function saveDataToFile(data, filename)
    local json = textutils.serialiseJSON(data)
    local file = fs.open(filename, "w")
    file.write(json)
    file.close()
end

local function loadDataFromFile(filename)
    local file = fs.open(filename, "r")
    local json = file.readAll()
    file.close()
    return textutils.unserialiseJSON(json)
end

