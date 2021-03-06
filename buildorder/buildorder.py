import sets

class DependencyError(Exception):
    def __init__(self):
        super(DependencyError, self).__init__("Unresolvable Project Dependencies")

def getBuildOrder(projects, dependencies = []):
    dependencyMap   = {}
    dependencyCount = {}
    dependencyFreeProjects = sets.Set(projects)

    for project in projects:
        dependencyMap[project]   = []
        dependencyCount[project] = 0

    for (dependency, project) in dependencies:
        dependencyMap[dependency].append(project)
        dependencyCount[project] += 1
        dependencyFreeProjects.discard(project)

    if len(dependencyFreeProjects) == 0:
        raise DependencyError()

    buildOrder = []

    for project in dependencyFreeProjects:
        buildOrder.append(project)
        resolveChildDependencies(project, dependencyMap, dependencyCount, buildOrder)

    if len(buildOrder) != len(projects):
        raise DependencyError()

    return buildOrder

def resolveChildDependencies(project, dependencyMap, dependencyCount, buildOrder):
    for dependentProject in dependencyMap[project]:
        dependencyCount[dependentProject] -= 1

        if dependencyCount[dependentProject] == 0:
            buildOrder.append(dependentProject)

            resolveChildDependencies(dependentProject, dependencyMap, dependencyCount, buildOrder)
