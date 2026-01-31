import diplib as dip

img = dip.ImageRead('vignette_shrunk.jpg')

scale = dip.CreateRadiusCoordinate(img.Sizes()) / 100
angle = dip.CreatePhiCoordinate(img.Sizes())
out = dip.AdaptiveGauss(img, [angle, scale], [1,5])

# Display the output
dip.Show(out)

# Save the output image
dip.ImageWrite(out, 'OutputImage.jpg')
