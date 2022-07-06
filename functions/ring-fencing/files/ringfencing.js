define([
    "knockout",
    "viewmodels/function",
    "viewmodels/concept-select",
    "bindings/select2-query",
    "views/components/widgets/concept-multiselect",
    "views/components/simple-switch",
    "arches",
], function (ko, FunctionViewModel, ConceptSelectViewModel, select2Query, conceptMultiselect, simpleSwitch, arches
) {
    //Classes
    class Rule {
        constructor(selectedNodeGroup, selectedNode, selectedVal, userGroups) {
            this.selectedNodeGroup = selectedNodeGroup;
            this.selectedNode = selectedNode;
            this.selectedVal = selectedVal;
            this.userGroups = userGroups;
        }

        rulesetToJson() {
            let ruleset = JSON.stringify(this.selectedNodeGroup()) + JSON.stringify(this.selectedNode()) + JSON.stringify(this.selectedVal())
            return ruleset
        }
    } // COMPLETE::

    //Methods
    const ruleExists = function (existingRules, newRule) {
        for (let i = 0; i < existingRules().length; i++) {
            if (existingRules()[i].selectedNodeGroup() == newRule.selectedNodeGroup()
                && existingRules()[i].selectedNode() == newRule.selectedNode()
                && existingRules()[i].selectedVal() == newRule.selectedVal())
                return true //Rule has been found
        }
        //REVIEW: Do I need to compare users? Since we're checking the building blocks first 
        //and then matching them into  the rule?
        return false; //Rule has not been found
    }

    const matchRule = function (existingRules, selectedNode, selectedNodeGroup, selectedVal) {
        for (let i = 0; i < existingRules().length; i++) {
            if (existingRules()[i].selectedNodeGroup() == selectedNodeGroup()
                && existingRules()[i].selectedNode() == selectedNode()
                && existingRules()[i].selectedVal() == selectedVal())
                return existingRules()[i]
        }
    }

    return ko.components.register(
        "views/components/functions/ringfencing",
        {
            viewModel: function (params) {
                FunctionViewModel.apply(this, arguments);
                var self = this;
                var nodegroups = {};
                this.rerender = ko.observable(true);
                this.cards = ko.observableArray();
                this.nodes = ko.observableArray([]);
                this.concepts = ko.observableArray([]);
                this.concept_nodes = ko.observableArray();
                this.concept_node = ko.observable();
                this.initialUsers = ko.observableArray();
                this.loading = ko.observable(false);
                this.triggering_nodegroups = params.config.triggering_nodegroups;

                ConceptSelectViewModel.apply(this, [params]);

                this.rules = params.config.rules;
                //new rule
                let newRule;
                //Blank rule values
                this.selectedNodeGroup = ko.observable();
                this.selectedNode = ko.observable();
                this.selectedVal = ko.observable();
                this.userGroups = ko.observableArray();

                // Use the custom /get/users endpoint to get up to date list of users. ** must add the endpoint
                $.getJSON("http://127.0.0.1:8000/get/users", function (data) {
                    self.initialUsers(data);
                }); //COMPLETE:

                // Requires push method when we get to multiple rules
                this.selectedNodeGroup.subscribe(function (val) {
                    self.triggering_nodegroups([val]);
                }); //COMPLETE:

                // Generates the list of nodegroups/cards to be used in the drop down
                this.graph.cards.forEach(function (card) {
                    var found = !!_.find(
                        this.graph.nodegroups,
                        function (nodegroup) {
                            return nodegroup.parentnodegroup_id === card.nodegroup_id;
                        },
                        this
                    );
                    if (!found && !(card.nodegroup_id in nodegroups)) {
                        card.id = card.nodegroup_id;
                        card.text = card.name; // Card Names
                        this.cards.push(card); // Add to cards array
                        nodegroups[card.nodegroup_id] = true;
                    }
                }, this); //NOTE: Might not be complete

                // This generates the list of nodes once nodegroup is selected
                this.selectedNodeGroup.subscribe(function () {
                    self.rerender(false); //Toggling rerender forces the node options to load in the select2 dropdown when the card changes
                    var nodes = self.graph.nodes
                        .filter(function (node) {
                            return node.nodegroup_id === self.selectedNodeGroup();
                        })
                        .map(function (node) {
                            node.id = node.nodeid;
                            node.text = node.name;
                            return node;
                        });
                    // re-write nodes to only concept type nodes
                    var nodes = nodes.filter(function (node) {
                        return node.datatype === "concept";
                    });
                    self.nodes.removeAll();
                    self.nodes(nodes);
                    self.rerender(true);
                }); //COMPLETE:

                // Compare initialUsers to userGroups
                // If they are identical, do nothing.
                // If there is a group in initialUsers but not in UserGroups, ADD
                // If there is a group in userGroups but not in initialUsers, DELETE

                // This compares userGroups to initialUsers and if one is missing, add it.
                this.initialUsers.subscribe(function (val) {
                    val.forEach(function (v, i) {
                        if (
                            self
                                .userGroups()
                                .some(
                                    (identity) => ko.unwrap(identity["identityName"]) === v.name
                                ) === false
                        ) {
                            var groupEntry = {
                                identityName: ko.unwrap(v.name),
                                identityId: ko.unwrap(v.id),
                                identityType: ko.unwrap(v.type),
                                identityVal: ko.observable(true),
                            };
                            self.userGroups.push(groupEntry);
                        }
                    });
                }); //COMPLETE:

                // Return concept list
                this.selectedNode.subscribe(function (val) {
                    var concept_node = self.graph.nodes.find(function (node) {
                        return node.nodeid === val;
                    });
                    self.concept_node(concept_node);
                }); //COMPLETE:

                this.selectedNodeGroup.valueHasMutated(); // Forces the node value to load into the node options when the template is renderer

                this.selectedVal.subscribe(function () {
                    // check if rule combination already exists, if so use the existing rule 
                    if (self.rules().length > 0) {
                        let existingRule = matchRule(self.rules, self.selectedNode, self.selectedNodeGroup, self.selectedVal)
                        if (existingRule) {
                            self.editRule(existingRule)

                        }
                    }

                }
                )//COMPLETE:

                //methods
                this.addRule = function () {
                        let newRule = new Rule(
                        this.selectedNodeGroup,
                        this.selectedNode,
                        this.selectedVal,
                        this.userGroups
                    );
                    if((newRule.selectedNodeGroup() == null
                    || newRule.selectedNode() == null
                    || newRule.selectedVal() == null)) alert("Can't add empty rule!")
                    else
                    if (ruleExists(self.rules, newRule)) alert("Rule already exists!");
                    else{
                        self.rules.push(newRule);
                    } 
                };
                //COMPLETE:

                this.removeRule = function () {
                    self.rules.remove(this);
                };//COMPLETE:

                this.editRule = function (rule) {
                    self.selectedNode(rule.selectedNode())
                    self.selectedNodeGroup(rule.selectedNodeGroup())
                    self.userGroups(rule.userGroups())
                    if(self.selectedVal() == null) self.selectedVal(rule.selectedVal())
                    self.rules.remove(rule)
                }// COMPLETE::

                this.getConceptText = function (uuid) {
                    let conceptName
                    $.ajax(
                        arches.urls.concept_value + "?valueid=" + ko.unwrap(uuid),
                        {
                            dataType: "json",
                            async: false
                        }
                    ).done(function (data) {
                        conceptName = data.value
                    });
                    return conceptName
                };//COMPLETE:

                this.getNodeText = function (uuid) {
                    const nodeText = self.graph.nodes.filter(function (node) {
                        return node.nodegroup_id === uuid
                    }).map(function (node) {
                        node.id = node.nodeid;
                        node.text = node.name;
                        return node.text;
                    });
                    return nodeText
                }//COMPLETE:
            },
            template: {
                require:
                    "text!templates/views/components/functions/ringfencing.htm",
            },
        }
    );
});