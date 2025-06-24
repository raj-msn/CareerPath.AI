import React, { useCallback, useState, useEffect } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Position,
  MarkerType,
  Handle,
} from 'reactflow';
import 'reactflow/dist/style.css';

// Custom node types for different phases
const PhaseNode = ({ data, selected }) => {
  return (
    <div className={`px-4 py-3 shadow-lg rounded-lg border-2 transition-all duration-200 min-w-48 max-w-64 ${
      selected 
        ? 'border-primary-500 shadow-primary-200' 
        : 'border-gray-300 hover:border-primary-300'
    } ${data.type === 'start' ? 'bg-green-50 border-green-300' : 
         data.type === 'end' ? 'bg-blue-50 border-blue-300' : 
         'bg-white'}`}>
      
      {/* Input handle (top) - except for start node */}
      {data.type !== 'start' && (
        <Handle
          type="target"
          position={Position.Top}
          style={{ background: '#3b82f6' }}
        />
      )}
      
      {/* Output handle (bottom) - except for end node */}
      {data.type !== 'end' && (
        <Handle
          type="source"
          position={Position.Bottom}
          style={{ background: '#10b981' }}
        />
      )}
      
      <div className="flex items-center space-x-2">
        <div className="text-lg">{data.emoji}</div>
        <div className="flex-1">
          <div className="font-semibold text-sm text-gray-800">{data.label}</div>
          {data.duration && (
            <div className="text-xs text-gray-500">{data.duration}</div>
          )}
        </div>
      </div>
      
      {data.description && (
        <div className="mt-2 pt-2 border-t border-gray-200">
          <div className="text-xs text-gray-600">{data.description}</div>
        </div>
      )}
      
      {data.skills && data.skills.length > 0 && (
        <div className="mt-2 pt-2 border-t border-gray-200">
          <div className="text-xs text-gray-600">
            {data.skills.slice(0, 3).map((skill, idx) => (
              <span key={idx} className="inline-block bg-gray-100 px-2 py-1 rounded mr-1 mb-1 text-xs">
                {skill}
              </span>
            ))}
            {data.skills.length > 3 && (
              <span className="text-gray-400 text-xs">+{data.skills.length - 3} more</span>
            )}
          </div>
        </div>
      )}

      {/* Resource Links Section */}
      {data.resources && data.resources.length > 0 && (
        <div className="mt-2 pt-2 border-t border-gray-200">
          <div className="text-xs font-medium text-gray-700 mb-1">📚 Resources:</div>
          <div className="space-y-1">
            {data.resources.slice(0, 2).map((resource, idx) => (
              <a
                key={idx}
                href={resource.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block text-xs text-blue-600 hover:text-blue-800 hover:underline truncate"
                onClick={(e) => e.stopPropagation()} // Prevent node selection when clicking links
              >
                🔗 {resource.title}
              </a>
            ))}
            {data.resources.length > 2 && (
              <div className="text-xs text-gray-400">+{data.resources.length - 2} more resources</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Helper function to get relevant resources for a learning phase
const getRelevantResources = (phase, resources, phaseIndex) => {
  if (!resources) return [];
  
  const phaseResources = [];
  const phaseSkills = phase.skills || [];
  const phaseName = (phase.phase || '').toLowerCase();
  
  // Match courses to phase skills
  if (resources.courses) {
    resources.courses.forEach(course => {
      const courseSkills = course.skills || [];
      const hasMatchingSkill = phaseSkills.some(phaseSkill => 
        courseSkills.some(courseSkill => 
          courseSkill.toLowerCase().includes(phaseSkill.toLowerCase()) ||
          phaseSkill.toLowerCase().includes(courseSkill.toLowerCase())
        )
      );
      
      // Also match by phase name or course level
      const matchesPhase = course.title.toLowerCase().includes(phaseName) ||
                          (phaseIndex === 0 && course.level === 'Beginner') ||
                          (phaseIndex > 0 && course.level === 'Intermediate') ||
                          (phaseIndex > 1 && course.level === 'Advanced');
      
      if (hasMatchingSkill || matchesPhase) {
        phaseResources.push({
          title: course.title,
          url: course.url || '#',
          type: 'course',
          provider: course.provider
        });
      }
    });
  }
  
  // Match certifications to phase
  if (resources.certifications && phaseIndex > 0) { // Show certs for later phases
    resources.certifications.forEach(cert => {
      const certSkills = cert.skills || [];
      const hasMatchingSkill = phaseSkills.some(phaseSkill => 
        certSkills.some(certSkill => 
          certSkill.toLowerCase().includes(phaseSkill.toLowerCase()) ||
          phaseSkill.toLowerCase().includes(certSkill.toLowerCase())
        )
      );
      
      if (hasMatchingSkill) {
        phaseResources.push({
          title: cert.title,
          url: '#', // Certifications might not have direct URLs
          type: 'certification',
          provider: cert.provider
        });
      }
    });
  }
  
  // Limit to 3 resources per phase to keep cards manageable
  return phaseResources.slice(0, 3);
};

// Custom edge with progress indicator
const nodeTypes = {
  phaseNode: PhaseNode,
};

const CareerRoadmapFlow = ({ learningPath, resources, className = '' }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState(null);

  // Remove defaultEdgeOptions to avoid conflicts

  // Convert learning path data to React Flow nodes and edges
  useEffect(() => {
    if (!learningPath || !learningPath.learning_phases) {
      // Default roadmap when no data - with proper spacing
      const defaultSpacing = 220; // Larger spacing for default view to match dynamic spacing
      const defaultNodes = [
        {
          id: 'start',
          type: 'phaseNode',
          position: { x: 50, y: 50 },
          data: { 
            label: 'Start Your Journey', 
            emoji: '🚀',
            type: 'start'
          },
        },
        {
          id: 'end',
          type: 'phaseNode', 
          position: { x: 50, y: 50 + defaultSpacing },
          data: { 
            label: 'Achieve Your Goal', 
            emoji: '🎯',
            type: 'end'
          },
        },
      ];

      const defaultEdges = [
        {
          id: 'start-end',
          source: 'start',
          target: 'end',
          animated: true,
          style: { stroke: '#3b82f6', strokeWidth: 2 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
          },
        },
      ];

      setNodes(defaultNodes);
      setEdges(defaultEdges);
      return;
    }

    // Generate nodes from learning phases
    const phaseNodes = [];
    const phaseEdges = [];
    const phases = learningPath.learning_phases;
    
    console.log('🎨 REACT FLOW: Generating nodes from learning path:', {
      phases_count: phases.length,
      timeline: learningPath.timeline,
      has_changes: !!learningPath.changes_made
    });
    
    // Start node with consistent spacing
    const startY = 50;
    phaseNodes.push({
      id: 'start',
      type: 'phaseNode',
      position: { x: 50, y: startY },
      data: { 
        label: 'Current Role', 
        emoji: '👨‍💻',
        type: 'start'
      },
    });

    // Phase nodes - with much better spacing calculation
    const baseNodeHeight = 140; // More accurate node height estimate
    const minSpacing = 80; // Larger gap between nodes
    const nodeSpacing = baseNodeHeight + minSpacing; // Total spacing = 220px between centers
    
    phases.forEach((phase, index) => {
      // Calculate position with proper spacing from start node
      const yPosition = startY + nodeSpacing + (index * nodeSpacing);
      
      // Get relevant resources for this phase
      const phaseResources = getRelevantResources(phase, resources, index);
      
      phaseNodes.push({
        id: `phase-${index}`,
        type: 'phaseNode',
        position: { x: 50, y: yPosition },
        data: {
          label: phase.phase || `Phase ${index + 1}`,
          duration: phase.duration,
          skills: phase.skills || [],
          description: phase.description,
          emoji: ['📚', '🎓', '🏆', '⭐', '🚀', '💡'][index % 6],
          resources: phaseResources,
        },
      });

      // Edge from previous node - Blue arrows show learning progression
      const sourceId = index === 0 ? 'start' : `phase-${index - 1}`;
      phaseEdges.push({
        id: `edge-${index}`,
        source: sourceId,
        target: `phase-${index}`,
        animated: true,
        style: { stroke: '#3b82f6', strokeWidth: 2 },
        markerEnd: {
          type: MarkerType.ArrowClosed,
        },
      });
    });

    // End node with proper spacing from last phase
    const endY = startY + (phases.length + 1) * nodeSpacing;
    phaseNodes.push({
      id: 'end',
      type: 'phaseNode',
      position: { x: 50, y: endY },
      data: { 
        label: 'Target Role', 
        emoji: '🎯',
        type: 'end'
      },
    });

    // Final edge - Green arrow shows goal achievement
    phaseEdges.push({
      id: `edge-final`,
      source: phases.length > 0 ? `phase-${phases.length - 1}` : 'start',
      target: 'end',
      animated: true,
      style: { stroke: '#10b981', strokeWidth: 3 },
      markerEnd: {
        type: MarkerType.ArrowClosed,
      },
    });

    // Update with smooth transitions
    setNodes((prevNodes) => {
      // If this is an update and we have previous nodes, try to preserve positions
      if (prevNodes.length > 2) { // More than just start/end
        const nodeMap = new Map(prevNodes.map(node => [node.id, node]));
        return phaseNodes.map(newNode => {
          const existingNode = nodeMap.get(newNode.id);
          if (existingNode) {
            // Preserve position and any user interactions
            return {
              ...newNode,
              position: existingNode.position,
            };
          }
          return newNode;
        });
      }
      return phaseNodes;
    });
    
    setEdges(phaseEdges);
    
    // Log the update for debugging
    console.log('🎨 REACT FLOW: Updated with', phaseNodes.length, 'nodes and', phaseEdges.length, 'edges');
    
  }, [learningPath]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
  }, []);

  if (!learningPath) {
    return (
      <div className={`flex items-center justify-center p-8 text-gray-500 ${className}`}>
        <div className="text-center">
          <div className="text-4xl mb-2">🗺️</div>
          <p className="text-lg font-medium">Interactive Career Roadmap</p>
          <p className="text-sm">Start a conversation to generate your personalized path!</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`w-full h-full ${className}`}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}

        fitView
        fitViewOptions={{ padding: 0.2 }}
        attributionPosition="bottom-left"
      >
        <Controls />
        <MiniMap 
          nodeStrokeColor={(n) => n.type === 'input' ? '#10b981' : '#3b82f6'}
          nodeColor={(n) => n.data.type === 'start' ? '#dcfce7' : 
                           n.data.type === 'end' ? '#dbeafe' : '#f9fafb'}
          nodeBorderRadius={8}
          className="!bg-gray-50"
        />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>

      {/* Side panel for selected node details */}
      {selectedNode && (
        <div className="absolute top-4 right-4 w-64 bg-white rounded-lg shadow-lg border p-4 z-10">
          <div className="flex justify-between items-start mb-3">
            <h3 className="font-semibold text-gray-800">{selectedNode.data.label}</h3>
            <button 
              onClick={() => setSelectedNode(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>
          
          {selectedNode.data.duration && (
            <p className="text-sm text-gray-600 mb-2">
              <strong>Duration:</strong> {selectedNode.data.duration}
            </p>
          )}
          
          {selectedNode.data.skills && selectedNode.data.skills.length > 0 && (
            <div className="mb-3">
              <p className="text-sm font-medium text-gray-700 mb-2">Skills to develop:</p>
              <div className="space-y-1">
                {selectedNode.data.skills.map((skill, idx) => (
                  <span key={idx} className="inline-block bg-primary-100 text-primary-800 px-2 py-1 rounded text-xs mr-1">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {selectedNode.data.resources && selectedNode.data.resources.length > 0 && (
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">📚 Recommended Resources:</p>
              <div className="space-y-2">
                {selectedNode.data.resources.map((resource, idx) => (
                  <a
                    key={idx}
                    href={resource.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block p-2 bg-blue-50 hover:bg-blue-100 rounded border text-sm transition-colors"
                  >
                    <div className="font-medium text-blue-800">🔗 {resource.title}</div>
                    {resource.provider && (
                      <div className="text-xs text-blue-600 mt-1">by {resource.provider}</div>
                    )}
                    <div className="text-xs text-blue-500 mt-1 capitalize">{resource.type}</div>
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CareerRoadmapFlow; 