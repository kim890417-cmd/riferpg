$outDir = "C:\Users\User\Desktop\life_rpg\art"

$animals = @{
    fox = 4201
    hamster = 4202
    cat = 4203
    dog = 4204
    fish = 4206
}

$prompts = @{
    # 🦊 여우
    "fox_baby"     = "超かわいい SD super deformed chibi baby fox cub, adorable 2D pixel art game sprite like maplestory, very big sparkly shiny eyes, tiny chubby round body, super cute orange fluffy fur, cute small paws and big ears, kawaii game character, pure white background, front standing"
    "fox_child"    = "超かわいい SD chibi baby fox standing up, cute 2D pixel art maplestory style, big glossy eyes, chubby cheeks, fluffy orange tail, tiny paws, kawaii game character, white background, front view"
    "fox_teen"     = "超かわいい SD chibi young fox growing, cute 2D pixel art maplestory, big sparkly eyes, playful pose, orange fur white chest, fluffy tail, kawaii game character, white background"
    "fox_adult"    = "超かわいい SD chibi adult fox, elegant 2D pixel art maplestory style, two fluffy golden tails, big cute eyes, mystical aura, kawaii game character, white background"
    "fox_legendary"= "超かわいい SD chibi nine-tailed fox gumiho, 2D pixel art maplestory style, nine fluffy golden tails, glowing cute eyes, magical sparkles, kawaii game character, white background"

    # 🐹 햄스터
    "hamster_baby"     = "超かわいい SD super deformed chibi baby hamster, adorable 2D pixel art maplestory style, very big sparkly eyes, tiny round pink chubby body no fur yet, kawaii game character, pure white background"
    "hamster_child"    = "超かわいい SD chibi baby hamster standing, 2D pixel art maplestory, big round eyes, puffed cheeks full of food, chubby round body, kawaii game character, white background"
    "hamster_teen"     = "超かわいい SD chibi growing hamster, cute 2D pixel art maplestory, big sparkly eyes, curious expression, tiny paws, chubby body, kawaii game character, white background"
    "hamster_adult"    = "超かわいい SD chibi hamster warrior, 2D pixel art maplestory style, big cute eyes, tiny wooden sword, brave determined face, kawaii game character, white background"
    "hamster_legendary"= "超かわいい SD chibi king hamster, 2D pixel art maplestory style, tiny golden crown, royal red cape, big sparkly eyes, majestic cute, kawaii game character, white background"

    # 🐱 고양이
    "cat_baby"     = "超かわいい SD super deformed chibi baby kitten, adorable 2D pixel art maplestory style, very big sparkly blue eyes, tiny fluffy grey body, pink nose, kawaii game character, pure white background"
    "cat_child"    = "超かわいい SD chibi baby kitten standing, cute 2D pixel art maplestory, big round eyes, playful pose, fluffy tail up, kawaii game character, white background"
    "cat_teen"     = "超かわいい SD chibi young cat, graceful 2D pixel art maplestory, big sparkling green eyes, elegant long tail, cute independent look, kawaii game character, white background"
    "cat_adult"    = "超かわいい SD chibi adult cat mage, 2D pixel art maplestory, purple glowing eyes, magical whiskers, star sparkles, kawaii game character, white background"
    "cat_legendary"= "超かわいい SD chibi legendary cat goddess, 2D pixel art maplestory, rainbow flowing fur, nine lives aura, big sparkling cosmic eyes, kawaii game character, white background"

    # 🐶 강아지
    "dog_baby"     = "超かわいい SD super deformed chibi baby puppy, adorable 2D pixel art maplestory style, very big sparkly innocent eyes, tiny round brown fluffy body, floppy ears, kawaii game character, pure white background"
    "dog_child"    = "超かわいい SD chibi puppy standing, cute 2D pixel art maplestory, big round eyes, chubby body, floppy ears, tail wagging, kawaii game character, white background"
    "dog_teen"     = "超かわいい SD chibi wolf pup growing, cute 2D pixel art maplestory, big sparkly blue eyes, silver-grey fur, alert pointed ears, kawaii game character, white background"
    "dog_adult"    = "超かわいい SD chibi wolf warrior, 2D pixel art maplestory, silver coat, big fierce yet cute eyes, noble stance, kawaii game character, white background"
    "dog_legendary"= "超かわいい SD chibi moon wolf guardian, 2D pixel art maplestory, starry night fur, aurora mane, big sparkling cosmic eyes, kawaii game character, white background"

    # 🐠 코이
    "fish_baby"     = "超かわいい SD super deformed chibi baby koi fish, adorable 2D pixel art maplestory style, very big sparkly eyes, tiny round orange body, swimming in water, kawaii game character, pure white background"
    "fish_child"    = "超かわいい SD chibi koi fish growing, cute 2D pixel art maplestory, big sparkly eyes, orange and white patterns, flowing fins, kawaii game character, white background"
    "fish_teen"     = "超かわいい SD chibi brocade koi fish, cute 2D pixel art maplestory, big cute eyes, beautiful red white gold patterns, elegant fins, kawaii game character, white background"
    "fish_adult"    = "超かわいい SD chibi golden koi fish, 2D pixel art maplestory style, big sparkling eyes, shining golden scales, long flowing fins, kawaii game character, white background"
    "fish_legendary"= "超かわいい SD chibi dragon evolved from koi, 2D pixel art maplestory style, cute dragon with koi features, big sparkly eyes, scales and fins, kawaii game character, white background"
}

$total = ($prompts.Keys | Measure-Object).Count
$i = 0

foreach ($key in $prompts.Keys) {
    $animal = $key.Split('_')[0]
    $stage = $key.Substring($animal.Length + 1)
    $seed = $animals[$animal]
    $prompt = $prompts[$key]
    $encoded = [System.Uri]::EscapeDataString($prompt)
    $outFile = Join-Path $outDir "char_${animal}_${stage}.webp"
    $url = "https://image.pollinations.ai/prompt/${encoded}?width=256&height=320&seed=${seed}&model=flux"

    $i++
    Write-Host ("[" + $i + "/" + $total + "] " + $animal + "_" + $stage + " ... ") -NoNewline

    try {
        Invoke-WebRequest -Uri $url -OutFile $outFile -TimeoutSec 60
        Write-Host "OK" -ForegroundColor Green
    } catch {
        Write-Host ("FAIL: " + $_) -ForegroundColor Red
    }

    Start-Sleep -Milliseconds 500
}

Write-Host ""
Write-Host ("Done! " + $i + " images generated") -ForegroundColor Green
