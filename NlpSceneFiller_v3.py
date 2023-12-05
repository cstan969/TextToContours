
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import pprint

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain

import matplotlib
matplotlib.use('Qt5Agg')  # or another interactive backend like 'Qt5Agg', 'GTK3Agg', etc.


class NlpSceneFiller:

    def scene_prompt(self, scene_id, update_prompt):
        #scene info stuffs
        self.scene_id = scene_id
        self.previous_scene_json_filename = '-'.join(['previous_scene_json',str(scene_id)]) + '.json'
        self.scene_json_filename = '-'.join(['scene_json',str(scene_id)]) + '.json'
        self.chat_history_filepath = '-'.join(['chat_history',str(scene_id)]) + '.json'

        #prompt stuffs
        self.update_prompt = update_prompt


        #LLM stuffs
        # self.llm = ChatOpenAI(model='gpt-4-1106-preview', temperature=0.7)
        self.llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.7)


        self._load_prompt_plot_and_save()


    def _load_prompt_plot_and_save(self):
        #load file
        try:
            with open(self.scene_json_filename,'r') as fp:
                self.previous_scene_json = json.load(fp)
        except:
            self.previous_scene_json = {}
        print('previous_scene_json: ', self.previous_scene_json)
        if 'previous_scene_description' in self.previous_scene_json:
            self.previous_scene_description = self.previous_scene_json['previous_scene_description']
        else:
            self.previous_scene_description = "This is the start of the scene and there is no description yet."

        #Manage conversation / Chat History
        try:
            with open(self.chat_history,'r') as fp:
                self.chat_history = json.load(fp)
            # self.chat_history.append(self.update_prompt)
        except:
            # self.chat_history = [self.update_prompt]
            self.chat_history = []

        #run prompt
        self._prompt_gpt()

        #save files (previous and current)
        with open(self.scene_json_filename,'w') as fp:
            json.dump(self.scene_json, fp, indent=4)
        with open(self.previous_scene_json_filename,'w') as fp:
            json.dump(self.previous_scene_json, fp, indent=4)
        with open(self.chat_history_filepath,'w') as fp:
            json.dump(self.chat_history,fp,indent=4)
        print('scenes saved')

        


        # print('type(self.previous_scene_json): ', type(self.previous_scene_json))
        # print('type(self.scene_json): ', type(self.scene_json))


        self._plot3d()

    #given the current json object, and the prompt from the user, generate a new json object
    def _prompt_gpt(self):
        template = """
        '''''
        ROLE: You are an expert area generator.  I will give you information about the area and what currently exists in the area.
        I will then request that you make some changes to what exists in an area.
        Take your time and step by step give me a list of operations to adjust the area as I requested.
        These steps might include finding the area to adjust, making changes to pre-existing objects, removing objects, deleting objects, or any combination thereof.
        Given the list of steps, generate or update the scene_objects_list as necessary.
        You operate in a 3D Space.
        You work in a X,Y,Z coordinate system. X denotes width, Y denotes height, Z denotes depth. 0.0,0.0,0.0 is the default space origin.
        All objects must be within the bounds of the scene.

        '''''
        Here is the current json representation of the current scene_json object:
        
        {previous_scene_json}

        '''''
        Here is the high level description of the current scene.  This should give some idea of the entities/objects in the string and their relative layout:

        {previous_scene_description}

        '''''
        Here is the chat history of the user.  You have already accounted for these updates.

        {chat_history}

        '''''
        Here is the current prompt from the user to either create or update the existing json scene:

        {update_prompt}

        '''''
        Required Output: You must format your output as a JSON dictionary that adheres to a given JSON schema instance with the following keys:
            "update_prompt": the update_prompt.
            "chat_history": the chat history as a list of strings.
            "task_reasoning": Explain to me in your own words what steps need to be taken in order to adjust the scene as I asked.  This may include deleting, adding, or updating existing entities.
            "previous_scene_description": the previous scene description.
            "new_scene_description": The new scene description after adjusting for the update_prompt.
            "Scene_name": the name of the scene.
            "Scene_x_size:" the size of the scene in the x dimension.
            "Scene_y_size": the size of the scene in the y dimension.
            "Scene_z_size": the size of the scene in the z dimensio.
            "Scene_objects_list": A list of dictionaries with keys.
                "object_name": unique name of the object.
                "object_description": a more detailed description of the object.
                "X": coordinate of the object on X axis.
                "dX": size of the object on the X axis.
                "Y": coordinate of the object on Y axis.
                "dY": size of the object on the Y axis.
                "Z": coordinate of the object on the Z axis.
                "dZ": size of the object on the Z axis.
        """
        prompt_from_template = PromptTemplate(template=template, input_variables=["previous_scene_json","chat_history", "previous_scene_description", "update_prompt"])
        llm_chain = LLMChain(prompt=prompt_from_template,llm=self.llm, verbose=True)
        response = llm_chain.run(previous_scene_json=str(self.previous_scene_json), update_prompt=self.update_prompt, chat_history=self.chat_history, previous_scene_description=self.previous_scene_description)
        print(response)
        try:
            response = json.loads(response)
        except:
            response = self._fix_json(response)
            response = json.loads(response)
        pprint.pprint(response)
        self.scene_json = response

    def _plot3d(self):
        # Function to create a list of vertices for a cube
        def create_cube_vertices(x, y, z, dx, dy, dz):
            return [
                [x, y, z],
                [x + dx, y, z],
                [x + dx, y + dy, z],
                [x, y + dy, z],
                [x, y, z + dz],
                [x + dx, y, z + dz],
                [x + dx, y + dy, z + dz],
                [x, y + dy, z + dz]
            ]
        # Function to create cube faces from vertices
        def create_cube_faces(vertices):
            return [
                [vertices[0], vertices[1], vertices[2], vertices[3]],
                [vertices[4], vertices[5], vertices[6], vertices[7]], 
                [vertices[0], vertices[3], vertices[7], vertices[4]], 
                [vertices[1], vertices[2], vertices[6], vertices[5]],
                [vertices[0], vertices[1], vertices[5], vertices[4]],
                [vertices[2], vertices[3], vertices[7], vertices[6]]
            ]
        
        def plot_scene(ax, scene_data):
            for obj in scene_data["Scene_objects_list"]:
                x, dx = obj["X"], obj["dX"]
                y, dy = obj["Y"], obj["dY"]
                z, dz = obj["Z"], obj["dZ"]
                vertices = create_cube_vertices(x, y, z, dx, dy, dz)
                faces = create_cube_faces(vertices)
                poly3d = Poly3DCollection(faces, alpha=0.5, edgecolors='k')
                ax.add_collection3d(poly3d)
            ax.set_xlim(0, scene_data["Scene_x_size"])
            ax.set_ylim(0, scene_data["Scene_y_size"])
            ax.set_zlim(0, scene_data["Scene_z_size"])
            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            ax.set_zlabel('Z axis')

        # Create a figure with two subplots
        fig = plt.figure(figsize=(20, 10))  # Adjust the size as needed
        ax1 = fig.add_subplot(121, projection='3d')  # Subplot for current scene
        ax2 = fig.add_subplot(122, projection='3d')  # Subplot for previous scene

        # Plot the current scene
        plot_scene(ax1, self.scene_json)
        ax1.set_title('Current Scene')

        # Plot the previous scene
        if self.previous_scene_json != {}:
            plot_scene(ax2, self.previous_scene_json)
            ax2.set_title('Previous Scene')

        # Show the plot
        plt.show()

    def _fix_json(self, json_to_fix):
        template = """I have some broken JSON below that I need to be able to run json.loads() on.  Can you fix it for me? Thanks.\n\n{question}"""
        prompt_from_template = PromptTemplate(template=template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt_from_template,llm=self.llm, verbose=True)
        response = llm_chain.run(json_to_fix)
        return response



# scene_filler = NlpSceneFiller()
# scene_filler.scene_prompt(
#     scene_id='test',
#     update_prompt='a large cat next to a small puppy'
# )

# scene_filler = NlpSceneFiller()
# scene_filler.scene_prompt(
#     scene_id='test',
#     update_prompt='make it three puppies'
# )

scene_filler = NlpSceneFiller()
scene_filler.scene_prompt(
    scene_id='test',
    update_prompt='make ones of the puppies be purple and slightly larger than the others.  Also add a horse in the background and make it green'
)

# scene_filler = NlpSceneFiller()
# scene_filler.scene_prompt(
#     scene_id='test',
#     update_prompt='the puppies are overlapping.  fix that.'
# )

# scene_filler = NlpSceneFiller()
# scene_filler.scene_prompt(
#     scene_id='test',
#     update_prompt='put the new puppies behind the first two as opposed to on top of the cat'
# )

