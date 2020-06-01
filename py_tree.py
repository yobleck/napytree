#yobleck
import math, time;
class Node(): #
    def __init__(self, data, iparent=None): #initializing...
        self.data = data; #value of node
        self.children = []; #list of children attached to node
        self.parent = iparent;

##############################
        
    def get_data(self): #get data from node   does nothing with children
        return self.data;

##############################
    
    def set_data(self, new_data):
        self.data = new_data;

##############################    
    
    def add_child(self, cdata):
        if(isinstance(cdata, Node)): #child is automatically made a node and user input is the data value of said node
            print("ERROR: child data value can't be a node to avoid confusion");
        else:
            self.children.append(Node(cdata, self));

##############################

    def set_parent(self, new_parent):
        if(isinstance(new_parent, Node)):
            self.parent = new_parent;

##############################    
    
    def get_parent(self):
        return self.parent;

##############################

    def list_children(self): #lists children as objects in memory
        return self.children;

##############################
    
    def list_children_data(self): #lists data values of children    unnecessary? maybe just use get_data on list_children?
        temp_list = [];
        for x in self.children: #there should be a better way to do this with the map() function but I couldn't get it to work
            temp_list.append(x.get_data());
        return temp_list;

##############################
    
    def search(self, param): #jank af, gathers all nodes then searches linearly. do I need tier?
        node_list = []; #stores return values from children
        if(self.data == param): #check if parent is param
            return self; #print("found", self, self.data);
        
        elif(self.children):
            for x in self.children:
               node_list.append(x.search(param)); #runs search on all children and saves to list TODO: compare to param here?
            
            for i in node_list: #goes through list and searches
                if(isinstance(i, Node)): #avoids whatever and where ever this Nonetype error is
                    if(i.get_data() == param): 
                        return i;
            
        return Node("search parameter not found"); #if all else fails

##############################
    
    def show(self, tier=0): #basic cli representation of the tree # TODO: interface with graphviz
        for i in range(0,tier):
            if(i == 0): #convoluted shit to try and make the tree more readable
                print("|", end="");
            if(i == tier-1 and tier-1 != 0):
                print("|", end="");
                print("---", end ="");
            else:
                print("----", end ="");
        print(self.data);
        for x in self.children:
            x.show(tier+1);

##############################
    
    def walk_tree(self, start, stop, return_type): #walk method   NCP = nearest common parent
        temp_start = self.search(start); #check to see if start and stop exist
        temp_stop = self.search(stop);
        if(temp_start.get_data() == "search parameter not found" or temp_stop.get_data() == "search parameter not found"):
            return Node("walk parameter not found"); #wont run if terms don't exist
        
        else:
            start_list_data = [temp_start.get_data()];
            stop_list_data = [temp_stop.get_data()];
            while(temp_start.get_parent() != None): #gets path to root node from start
                start_list_data.append(temp_start.get_parent().get_data()); #get parent
                temp_start = temp_start.get_parent(); #set to parent
            
            while(temp_stop.get_parent() != None): #^^^ditto from start
                stop_list_data.append(temp_stop.get_parent().get_data());
                temp_stop = temp_stop.get_parent();
            
            #print(start_list_data);
            #print(stop_list_data);
            
            tree_style = ""; #for checking if start and stop are in same branch or not
            if(not start in stop_list_data and not stop in start_list_data): #not in same branch
                while(start_list_data[-2] == stop_list_data[-2]): #removes nodes above NCP   
                    del start_list_data[-1];
                    del stop_list_data[-1];
                tree_style = "two_branch";
            
            elif(start in stop_list_data): #start is closer to root and in stop's list
                start_list_data.clear(); #used to check which list to return
                stop_list_data = stop_list_data[:stop_list_data.index(start)+1]; #cutting off list so its just stop to start
                stop_list_data.reverse(); #only has to be done for this way
                tree_style = "one_branch";
                
            elif(stop in start_list_data): #stop is closer to root and in start's list
                stop_list_data.clear();
                start_list_data = start_list_data[:start_list_data.index(stop)+1]; #^^^ or start to stop
                tree_style = "one_branch";
            
            
            if(return_type == "tree" and tree_style == "one_branch"): #TODO
                pass;
            
            if(return_type == "list" and tree_style == "one_branch"): #return list going from start to stop
                if(not start_list_data):
                    return stop_list_data;
                elif(not stop_list_data):
                    return start_list_data;
            
            if(return_type == "tree" and tree_style == "two_branch"): #return new tree with root = NCP for start and stop
                walk_tree = Node(start_list_data[-1]); #create root node
                walk_tree.add_child(start_list_data[-2]); #initialize start branch
                walk_tree.add_child(stop_list_data[-2]); #initialize stop branch
                
                temp_node = walk_tree.list_children()[0];
                for i in reversed(start_list_data[:-2]): #loop to branch left down start_list_data
                    temp_node.add_child(i);
                    temp_node = temp_node.list_children()[0];
                    
                temp_node1 = walk_tree.list_children()[1];
                for i in reversed(stop_list_data[:-2]): #loop to branch right down stop_list_data
                    temp_node1.add_child(i);
                    temp_node1 = temp_node1.list_children()[0];
                return walk_tree;
            
            elif(return_type == "list" and tree_style == "two_branch"): #just returns list going from start to NCP to stop
                output_list = start_list_data[0:len(start_list_data)]; #start list up to NCP
                output_list.extend(reversed(stop_list_data[0:len(stop_list_data)-1])); #reverse of stop list not including NCP
                return output_list;

##############################
    #TODO:merge trees method. should this be a function outside of node? use add_child and set_parent
    


test = Node(5);
test.add_child(Node(6));
test.add_child(Node(10));
test.add_child(Node(18));
test.list_children()[1].add_child(Node(12));

print(test.get_data());
print(test.list_children());
print(test.list_child_data());
print(test.search(11).get_data());
test.show(); 
