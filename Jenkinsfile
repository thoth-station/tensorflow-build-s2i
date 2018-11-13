def operatingSystem = env.OPERATING_SYSTEM ?: "fedora26"
def registry = env.REGISTRY ?: "registry.fedoraproject.org/f26/s2i-core"
def pythonVersion = env.PYTHON_VERSION ?: "3.6"
def pythonVersionNoDecimal = pythonVersion.replaceAll("[^a-zA-Z0-9]+","")

def project = "tensorflow"

node {
  def builderImageStream = ''
  def buildJob = ''

  openshift.withCluster() {
    openshift.withProject(project) {
      try {
        stage("Build Image") {
          def tensorflowImageTemplate = openshift.selector("template", "tensorflow-build-image").object()
          builderImageStream = openshift.process(
            tensorflowImageTemplate,
            "-p", "APPLICATION_NAME=tf-${operatingSystem}-build-image-${pythonVersionNoDecimal}",
            "-p", "S2I_IMAGE=${registry}",
            "-p", "DOCKER_FILE_PATH=Dockerfile.${operatingSystem}",
            "-p", "NB_PYTHON_VER=${pythonVersion}"
          )
          def thing = openshift.create(builderImageStream)
          thing.describe()
          thing.narrow('bc').logs('-f')
        }

        stage("Build Job") {
          def tensorflowJobTemplate = openshift.selector("template", "tensorflow-build-job").object()
          buildJob = openshift.process(
            tensorflowJobTemplate,
            "-p", "APPLICATION_NAME=tf-${operatingSystem}-build-job-${pythonVersionNoDecimal}",
            "-p", "BUILDER_IMAGESTREAM=tf-${operatingSystem}-build-image-${pythonVersionNoDecimal}",
            "-p", "NB_PYTHON_VER=${pythonVersion}",
            "-p", "SESHETA_GITHUB_ACCESS_TOKEN=test"
          )
          def thing = openshift.create(buildJob)
          def pods = thing.related('pods')
          pods.untilEach {
            return (it.object().status.phase == "Running")
          }
          pods.logs("-f")
        }
      } catch (e) {
        echo e.toString()
        throw e
      } finally {
        stage("Cleanup") {
          openshift.delete(builderImageStream)
          openshift.delete(buildJob)
        }
      }
    }
  }
}
