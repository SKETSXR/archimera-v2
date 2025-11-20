# Idea

The main idea is to:

1. Have a streamlit application on which the users will upload data, which would result in a searchable library. The users will add the following for a specific asset:

    1. Metadata: This will include the following information:

        1. Client Name
        2. Project Name
        3. Asset ID (unique identifier)
        4. Category (eg. wardrobe)
        5. Added by
    2. Sketch: Here the user will upload sketches (different views), atleast one to be added:

        1. Elevated View
        2. Plan View
        3. Sectional View
    3. Tags: Here the user will select tags for the asset, from a predefined-set of tags.
    4. CADs: Here the user will upload CADs (different views) DWG files, atleast one to be added:

        1. Elevated View
        2. Plan View
        3. Sectional View

2. When a user uploads data, I want these informations to be stored in MongoDB database.

3. Once enough data is collected, I will be taking out these informations in a structured way, such that I can train models for CAD similarity search.

4. I will be using CLIP to generate embeddings for Sketch (one per view), and combine tag embedding to each of them.

5. I will be using autocad (pyautocad) (this will be running on a Windows Backend), to extract metadata from CAD files (one per view) and raster images (one per view), and then this would be passed through CLIP to generate per view embedding (metadata and image embedding would be combined per view).

6. I will create cartesian product based mapping to get input output pairs (sketch+tag embedding as input, CAD+metadata embedding as output).

7. I will then have two projection heads, one for input and the other for output, which will these embeddings to a shared space, where they are very close to each other (plan to train this through contrastive loss, and Recall@K as a evaluation metric). Note that once the model is trained, I will be saving the CAD embeddings.

8. For a query sketch, and tags. The projection head which was responsible for bringing input to shared space, would only be used, and then we will compare similarity with all CADs, and return most similar CADs.
