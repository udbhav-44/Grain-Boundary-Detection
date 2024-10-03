Tentative Task :

1. Grain Boundary Detection
2. Grain Segmentation
3. Grain Classification
4. Grain Tracking
5. Grain Counting
6. Grain Size Analysis
7. Grain Shape Analysis
8. Grain Orientation Analysis
9.  Grain Morphology Analysis
10. Grain Size Distribution Analysis
11. Grain Boundary Characterization
12. Grain Boundary Migration Analysis
13. Grain Boundary Energy Analysis
14. Grain Boundary Stability Analysis
15. Grain Boundary Segregation Analysis
16. Grain Boundary Texture Analysis
17. Grain Boundary Defect Analysis
18. Grain Boundary Etching Analysis



## 1. Grain Boundary Detection
1. [x] Gray Scale Conversion (if image is not in gray scale): 
2. [x] Gaussian Blur (to reduce noise and detail)
3. [x] Morphological Operations (Dilation, Erosion) 
   1. [x] Dilation : 	
   - 	**Used for**:
  	Expanding boundaries and Filling small gaps and connecting regions.
   - 	**Structuring Element**:
  	The operation compares each pixel with its neighborhood defined by a kernel (where the kernel is white, the pixel will be set to white).
   - 	**Iterations**:
  	In watershed algorithm, dilation helps enlarge the background regions to clearly distinguish objects from the background.
    2. [x] Erosion :
   - 	**Used for**:
		The opposite of dilation, erosion shrinks the white areas by changing white pixels to black.
   - 	**Noise Removal**: Helps shrink white regions.
4. [ ] Graph Segmentation
5. [ ] Color Mapping
6. [ ] Edge Detection
7. [ ] Overlaying Edges







