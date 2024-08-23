RECOIL = 0
SLEEP = 1
function main()
    while true do
        if IsKeyLockOn("capslock") then
            if IsMouseButtonPressed(1) then
                MoveMouseRelative(0, RECOIL)
                Sleep(SLEEP)
            end
        end
    end
end

main()