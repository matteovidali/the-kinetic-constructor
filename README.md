# Sequence_Constructor

bugs:

when dragging a pictograph arrow, if user accidentally right clicks, it messes with the arrow placement logic. It should ignore this instead.

add highlighting over the graphical object that you would select if you clicked at that moment

use the preprocessed letter dictionary to find the only letter group that could match before running comparisons


#####

plan to optimize option picker:

#####

It appears to be not filtering them out based on thumb orientation anymore and instead giving me every possible outcome that can result from my current specific position. It should be looking at each hand's individual thumb orientation.

Here's another idea that popped into my head: What if instead of looking for options that already match the thumb orientation, it looks for pairs and then assigns them thumb orientation based on the logic. Let's review the logic:

Let's say the user selects this for their first pictograph:
( key: letter,start_position,end_position,blue_color,blue_motion_type,blue_rotation_direction,blue_turns,blue_start_location,blue_end_location,blue_start_orientation,blue_end_orientation,blue_start_layer,blue_end_layer,red_color,red_motion_type,red_turns,red_rotation_direction,red_start_location,red_end_location,red_start_orientation,red_end_orientation,red_start_layer,red_end_layer,optimal_blue_location,optimal_red_location)

A,alpha1,alpha2,blue,pro,cw,0,s,w,in,in,1,1,red,pro,0,cw,n,e,in,in,1,1,,


It should look at the end position (alpha2) and get every possible pictograph that can end in that end position. Then instead of doing a filter to see if the thumb orientations match, it should look at the current situation and applies logic to set the thumb orientation. The user in this example picked something who end orientations are both in. 

Let's look at what this would mean. For each motion in the pictograph that follows, its end orientation will be determined by the start orientation (aka the end orientation of the user's selection, A). For a pro motion, the end orientation will match the start orientation(in to in or out to out). For an anti,  the orienation will swap (out to in or in to out). 

I'm thinking I could have a simplified dataframe that doesn't take into account the orientations and then we just assign them later in the program. 

the problem I see with that is that I'm relying on the dataframe to hold optimal location information for certain entries, but the majority of the entries don't have it. So maybe I need to offload the optimal location info to a different entry. It's important that there's specific optimal location info for every combination of out and in because the orientation changes the way the svgs look. So we can't get rid of orientations in my dataset entirely. But it seems like it migh make it faster to generate the options if I have a dataframe which is focused just on optimal locations and another that is focused more on generating the options when populating them.

My concern is that it will still have to go through the optimal locations engine when it's placing these pictographs, but maybe I can prevent it from iterating over that info except in special cases when it's necessary. I could have another mapping which just states whenhter or not a particular combination needs optimal locations or not. 

Now a final idea of mine which might speed things up tremendously is to generate a pictograph image for every single pictograph. This would be a lot of work up front but it would mean we don't have to actually create and set the items in the scene for every single pictograph. Instead it could be a list of thumbnails assoicated with the relevant line in the dataframe. That line in the dataframe could jsut be a link to the thumbnail. In theory this would be the best option because then presumably all we'd be passing aroud in the program would be the line of info like this:

"F,beta4,alpha3,blue,pro,cw,0,w,n,out,out,1,1,red,anti,0,cw,w,s,out,in,1,1,,"
Along with an image file. We wouldn't have to generate every scene and set every item and render every svg individually. 

what are your thoughts on my ideas and how can I help you to help me execute them?

 

###

GPT
Your ideas for optimization have merit and here’s a breakdown of how each could be implemented or considered:

1. Assigning Thumb Orientations Dynamically:
Instead of filtering options based on thumb orientation, you can select options based on end positions and then programmatically assign the thumb orientations. You can encapsulate this logic in a method, which can be beneficial in simplifying your DataFrame and reducing the complexity of your queries.

For instance:

python
Copy code
def assign_thumb_orientation(start_orientation: str, motion_type: str) -> str:
    if motion_type == "pro":
        return start_orientation
    elif motion_type == "anti":
        return "out" if start_orientation == "in" else "in"

# When creating options, use this function to determine end orientations:
red_end_orientation = assign_thumb_orientation(red_start_orientation, red_motion_type)
blue_end_orientation = assign_thumb_orientation(blue_start_orientation, blue_motion_type)
2. Separating Optimal Location Data:
Creating a separate structure for optimal locations is a good approach if the optimal location data is sparse. This can significantly reduce the amount of data you need to filter through for most pictographs, only querying the optimal locations when necessary.

3. Pre-generating Pictograph Images:
This is likely the most significant performance optimization. Rendering images instead of constructing pictograph scenes in real-time would drastically reduce the computational overhead. This process is known as caching and is a common strategy for improving performance in computer graphics.

You will need to pre-generate and store an image for every pictograph.
Store the images in an accessible directory structure or database.
Map each image to the corresponding data row, so you can easily retrieve it.
This approach does come with trade-offs:

Storage: You’ll need enough storage to save an image for every possible pictograph.
Upfront Time: The initial generation of all pictograph images could be time-consuming.
Flexibility: You lose some flexibility as any change in pictograph appearance would require regenerating all images.
Execution of the Ideas:
To implement these ideas, you can follow these steps:

Dynamic Orientation Assignment: Refactor your code to use the new function for assigning thumb orientations dynamically as options are generated.

Optimal Location Data Separation: Create a new data structure (like a dictionary or database) that maps specific position combinations to optimal locations. Update your code to query this data only when needed.

Image Caching:

Generate images for each pictograph and save them with a naming convention that allows you to easily map them to data rows.
Replace the logic in your UI that constructs scenes with logic that loads and displays images.
Ensure that your UI components that display options are optimized for image display (like using QLabel with setPixmap).
Testing: After implementing each optimization, test the performance impact. Profiling tools can help you verify if the changes are effective.

Code Maintenance: With these changes, your code complexity may increase, so consider adding documentation and tests to ensure maintainability.

Implementing these ideas should significantly improve the performance of your application, especially if you combine them. Each has its complexities and would require careful planning and execution.