FROM ruby:3.2-alpine

WORKDIR /site

# Install dependencies
RUN apk add --no-cache build-base

# Copy dependency files
COPY Gemfile* ./

# Install gems
RUN bundle install

# Copy site files
COPY . .

# Expose port
EXPOSE 4000

# Run Jekyll
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--livereload"]
