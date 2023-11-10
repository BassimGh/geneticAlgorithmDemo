from os import write
from PIL import Image, ImageDraw
import pprint
import random
import time
import pickle
from glob import glob

targetimg = Image.open("/Users/bassim/Documents/python/Genetic Algorithms/MonaLisa.jpg")
targetData = targetimg.getdata()
width, height = targetimg.size

def getColorRange(img):
    img_data = img.getdata()
    colorRange = []
    for pixel in img_data:
        if pixel not in colorRange:
            colorRange.append(pixel)
    print(len(colorRange))
    return colorRange

# colorRange = getColorRange(targetimg)

def generateCircle():
    pos1 = (random.randint(0,width-2), random.randint(0,height-2))
    pos2 = (random.randint(pos1[0] + 2,width), random.randint(pos1[1] + 2,height))
    ellipse = {
        "pos1" : pos1 ,
        "pos2" : pos2 ,
        "color" : random.choice(colorRange) + (random.randint(0,255),)
    }
    return ellipse

def generatePopulation(size):
    population = []

    # # for each image
    # for i in range(size):
    #     ellipses = []
    #     # for each line in images
    #     for j in range(ellipse_count):
    #         ellipse = generateCircle()
    #         ellipses.append(ellipse)
    #     population.append(ellipses)

    for i in range(size):
        ellipses = []
        ellipse = generateCircle()
        ellipses.append(ellipse)
        population.append(ellipses)

    return population

def fitness(ellipses):
    img = Image.new("RGBA", (width,height), color=1)
    for circle in ellipses:
        overlay = Image.new("RGBA", (width,height), color=1)
        draw = ImageDraw.Draw(overlay)
        draw.ellipse([circle["pos1"], circle["pos2"]], fill=circle["color"])
        img = Image.alpha_composite(img, overlay)

    img = img.convert("RGB")
    img_data = img.getdata()
    diff = 0
    for i in range(len(img_data)):
        r1,g1,b1 = img_data[i]
        r2,g2,b2 = targetData[i]

        delta_r = abs(r2 - r1)
        delta_g = abs(g2 - g1)
        delta_b = abs(b2 - b1)

        diff += delta_r ** 2 + delta_g ** 2 + delta_b ** 2
    
    return diff    

def selection(population):
    scores = []
    smallest_diff = 100000000000000000000000
    biggest_diff = 0
    pool = []

    images = []
    bestImage = []

    for image in population:
        score = fitness(image)

        if score < smallest_diff:
            smallest_diff = score
            bestImage = image
        if score > biggest_diff:
            biggest_diff = score
        scores.append(score)
    
    for i in range(len(population)):
        num =  (1 / (biggest_diff + 1 - smallest_diff)) * (scores[i] - smallest_diff)
        for j in range(int( len(population) -  num * len(population) )):
            pool.append(population[i])
    
    return pool, scores, bestImage, smallest_diff

def crossover(population, pool, scores):
    new_population = []
    for i in range(len(population)):
        parentA = random.choice(pool)
        parentB = random.choice(pool)

        half = len(parentA)//2
        child = []

        for j in range(half):
            child.append(parentA[j])

        for j in range(half, len(parentB)):
            child.append(parentB[j])

        child_fitness = fitness(child)

        if child_fitness < scores[i]:
            scores[i] = child_fitness
            new_population.append(child)
        else:
            new_population.append(population[i])
    return new_population, scores

def mutation(population, scores):
    mutation_rate = 0.005
    new_population = []
    # for each image
    for i, image in enumerate(population):
        # for each ellipse in an image
        new_ellipses = []
        for ellipse in image:
            if random.random() < mutation_rate:
                new_ellipse = generateCircle()
                new_ellipses.append(new_ellipse)
            else:
                new_ellipses.append(ellipse)

        # new_population.append(new_ellipses)


        new_score = fitness(new_ellipses)

        if new_score < scores[i]:
            scores[i] = new_score
            new_population.append(new_ellipses)
        else:
            new_population.append(population[i])

    return new_population

def imagify(image_data):
    img = Image.new("RGBA", (width,height), color="white")
    for ellipse in image_data:
        overlay = Image.new("RGBA", (width,height), color=1)
        draw = ImageDraw.Draw(overlay)
        draw.ellipse([ellipse["pos1"], ellipse["pos2"]], fill=ellipse["color"])
        img = Image.alpha_composite(img, overlay)
    return img

def main():
    init = time.time()

    best_images = []
    generations = 1000000000000000000000000000000000000000000000000000

    file = open("population.txt")

    population = generatePopulation(10)
    best_scores = []
    circle_count = 1
    for i in range(generations):
        before = circle_count
        if i <= 10 and i >= 1:
            best_scores.append(smallest_diff)
        if i > 10:
            best_scores.pop(0)
            best_scores.append(smallest_diff)
            if best_scores[0] == best_scores[9]:
                for circles in population:
                    circles.append(generateCircle())
                circle_count += 1
                # img.show()

        pool, scores, bestImage, smallest_diff = selection(population)
        population, scores = crossover(population,pool, scores)
        population = mutation(population, scores)

        if i == 0:
            img = imagify(bestImage)
            img.save(f"/Users/bassim/Documents/python/Genetic Algorithms/circles/{circle_count}.png")
        if circle_count != before:
            img = imagify(bestImage)
            img.save(f"/Users/bassim/Documents/python/Genetic Algorithms/circles/{circle_count}.png")

        # if i % 10:
        #     pickle.dump("poop", file)

        print("generation: ", i, ", ellipse count: ", circle_count)
        print("Smallest diff: ", smallest_diff)
        best_images.append(bestImage)
    
    img = imagify(best_images[generations-1])
    img.save("best.png")

    print(generations," generations took ", time.time() - init, " seconds")

# main()

file = open("population.pkl","w")

l = [1,2,3]

pickle.dump(l,file)

file.close()