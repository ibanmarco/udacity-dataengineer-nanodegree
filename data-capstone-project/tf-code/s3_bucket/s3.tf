####################################################################
# S3 Bucket

resource "aws_s3_bucket" "etl_analysis" {
  bucket = "${lower(var.project)}-bucket"
  acl    = "private"
}

resource "null_resource" "clone_repo_and_keep_csv" {
  provisioner "local-exec" {
    command = "cd data && git clone git@github.com:CSSEGISandData/COVID-19.git && for item in $(find COVID-19 | egrep -vi 'csv|\.git'); do rm -f $item; done"
  }
}

resource "null_resource" "remove_and_upload_to_s3" {
  depends_on = [clone_repo_and_keep_csv]
  provisioner "local-exec" {
    command = "aws s3 sync ${path.module}/to_s3 s3://${aws_s3_bucket.etl_analysis.id} --delete --region ${var.aws_region}"
  }
}


